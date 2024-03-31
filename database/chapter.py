from sys import maxsize
from typing import Optional

from database.data import \
    Chapter, \
    ChapterSlicer, \
    ChapterStyle
from database.sqlite import commit, fetchall, sqlescape

_TABLE = 'chapter'
_COLUMN_CID = 'cid'  # UUID.
_COLUMN_VID = 'vid'
_COLUMN_TRIGGER = 'trigger'  # uid.
_COLUMN_SLICER = 'slicer'
_COLUMN_STYLE = 'style'
_COLUMN_START = 'start'  # in seconds.
_COLUMN_LANG = 'lang'  # language code.
_COLUMN_CHAPTER = 'chapter'
_COLUMN_SUMMARY = 'summary'
_COLUMN_REFINED = 'refined'
_COLUMN_CREATE_TIMESTAMP = 'create_timestamp'
_COLUMN_UPDATE_TIMESTAMP = 'update_timestamp'


def create_chapter_table():
    commit(f'''
        CREATE TABLE IF NOT EXISTS {_TABLE} (
            {_COLUMN_CID}     TEXT NOT NULL PRIMARY KEY,
            {_COLUMN_VID}     TEXT NOT NULL DEFAULT '',
            {_COLUMN_TRIGGER} TEXT NOT NULL DEFAULT '',
            {_COLUMN_SLICER}  TEXT NOT NULL DEFAULT '',
            {_COLUMN_STYLE}   TEXT NOT NULL DEFAULT '',
            {_COLUMN_START}   INTEGER NOT NULL DEFAULT 0,
            {_COLUMN_LANG}    TEXT NOT NULL DEFAULT '',
            {_COLUMN_CHAPTER} TEXT NOT NULL DEFAULT '',
            {_COLUMN_SUMMARY} TEXT NOT NULL DEFAULT '',
            {_COLUMN_REFINED} INTEGER NOT NULL DEFAULT 0,
            {_COLUMN_CREATE_TIMESTAMP} INTEGER NOT NULL DEFAULT 0,
            {_COLUMN_UPDATE_TIMESTAMP} INTEGER NOT NULL DEFAULT 0
        )
        ''')
    commit(f'''
        CREATE INDEX IF NOT EXISTS idx_{_COLUMN_TRIGGER}
        ON {_TABLE} ({_COLUMN_TRIGGER})
        ''')
    commit(f'''
        CREATE INDEX IF NOT EXISTS idx_{_COLUMN_VID}
        ON {_TABLE} ({_COLUMN_VID})
        ''')
    commit(f'''
        CREATE INDEX IF NOT EXISTS idx_{_COLUMN_CREATE_TIMESTAMP}
        ON {_TABLE} ({_COLUMN_CREATE_TIMESTAMP})
        ''')
    commit(f'''
        CREATE INDEX IF NOT EXISTS idx_{_COLUMN_UPDATE_TIMESTAMP}
        ON {_TABLE} ({_COLUMN_UPDATE_TIMESTAMP})
        ''')


def find_chapter_by_cid(cid: str) -> Optional[Chapter]:
    res = fetchall(f'''
        SELECT
              {_COLUMN_CID},
              {_COLUMN_VID},
              {_COLUMN_TRIGGER},
              {_COLUMN_SLICER},
              {_COLUMN_STYLE},
              {_COLUMN_START},
              {_COLUMN_LANG},
              {_COLUMN_CHAPTER},
              {_COLUMN_SUMMARY},
              {_COLUMN_REFINED}
         FROM {_TABLE}
        WHERE {_COLUMN_CID} = '{sqlescape(cid)}'
        LIMIT 1
        ''')

    if not res:
        return None

    res = res[0]
    return Chapter(
        cid=res[0],
        vid=res[1],
        trigger=res[2],
        slicer=res[3],
        style=res[4],
        start=res[5],
        lang=res[6],
        chapter=res[7],
        summary=res[8],
        refined=res[9],
    )


def find_chapters_by_vid(vid: str, limit: int = maxsize) -> list[Chapter]:
    # Just ensure that there is no way for users to list all the videos we have
    # in the database. Such usage is not required for our extension to function.
    if vid == 'stub_vid':
        return []
    
    res = fetchall(f'''
        SELECT
              {_COLUMN_CID},
              {_COLUMN_VID},
              {_COLUMN_TRIGGER},
              {_COLUMN_SLICER},
              {_COLUMN_STYLE},
              {_COLUMN_START},
              {_COLUMN_LANG},
              {_COLUMN_CHAPTER},
              {_COLUMN_SUMMARY},
              {_COLUMN_REFINED}
         FROM {_TABLE}
        WHERE {_COLUMN_VID} = '{sqlescape(vid)}'
        ORDER BY {_COLUMN_START} ASC
        LIMIT {limit}
        ''')
    return list(map(lambda r: Chapter(
        cid=r[0],
        vid=r[1],
        trigger=r[2],
        slicer=r[3],
        style=r[4],
        start=r[5],
        lang=r[6],
        chapter=r[7],
        summary=r[8],
        refined=r[9],
    ), res))


def insert_chapters(chapters: list[Chapter]):
    for c in chapters:
        _insert_chapter(c)


def _insert_chapter(chapter: Chapter):
    commit(f'''
        INSERT INTO {_TABLE} (
            {_COLUMN_CID},
            {_COLUMN_VID},
            {_COLUMN_TRIGGER},
            {_COLUMN_SLICER},
            {_COLUMN_STYLE},
            {_COLUMN_START},
            {_COLUMN_LANG},
            {_COLUMN_CHAPTER},
            {_COLUMN_SUMMARY},
            {_COLUMN_REFINED},
            {_COLUMN_CREATE_TIMESTAMP},
            {_COLUMN_UPDATE_TIMESTAMP}
        ) VALUES (
            '{sqlescape(chapter.cid)}',
            '{sqlescape(chapter.vid)}',
            '{sqlescape(chapter.trigger)}',
            '{sqlescape(chapter.slicer)}',
            '{sqlescape(chapter.style)}',
             {chapter.start},
            '{sqlescape(chapter.lang)}',
            '{sqlescape(chapter.chapter)}',
            '{sqlescape(chapter.summary)}',
             {chapter.refined},
             STRFTIME('%s', 'NOW'),
             STRFTIME('%s', 'NOW')
        )
        ''')


def delete_chapters_by_vid(vid: str):
    commit(f'''
        DELETE FROM {_TABLE}
        WHERE {_COLUMN_VID} = '{sqlescape(vid)}'
        ''')


def insert_complete_video_summary(
    vid: str,
    video_summary: str,
    lang: str,
    trigger: str,
):
    # A bit of a hack. Let's represent the complete video summary
    # as a "Chapter".
    # TODO refactor: do this properly?
    video_summary_chapter = Chapter(
        cid=get_complete_video_summary_cid(vid),
        summary = video_summary,
        # Make sure not to use the same `vid` as for actual chapters,
        # because otherwise it will look like a regular chapter to the rest
        # of the app, e.g. it would return it from `find_chapters_by_vid`
        vid='stub_vid',
        trigger=trigger,
        # TODO not sure if this is correct
        style=ChapterStyle.MARKDOWN.value,
        lang=lang,
        # The below ones are just stubs, they don't make sense for
        # a "video_summary".
        slicer=ChapterSlicer.OPENAI.value,
        start=0,
        chapter="",
    )
    _insert_chapter(video_summary_chapter)


def find_complete_video_summary(vid: str) -> str:
    res = find_chapter_by_cid(get_complete_video_summary_cid(vid))
    if res is None:
        return None
    return res.summary


def delete_complete_video_summary(vid: str):
    cid = get_complete_video_summary_cid(vid)
    commit(f'''
        DELETE FROM {_TABLE}
        WHERE {_COLUMN_CID} = '{sqlescape(cid)}'
        ''')


def get_complete_video_summary_cid(vid: str):
    return f'{vid}_video_summary'
