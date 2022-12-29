from modules.handlers import subtitle_handler
import pytest

# Fixtures

@pytest.fixture
def test_handler():
    return subtitle_handler.SubtitleHandler()


# Tests

def test_download_subtitles(test_handler):
    subtitles = test_handler.download_subtitles('shigatsu wa kimi no uso')
    assert (
        len(subtitles) > 0 and
        subtitles.content.values[0] == '（かをり）ん？　うん？'
    )

def test_update_subtitles_df(test_handler):
    new_df = test_handler.download_subtitles('shigatsu wa kimi no uso')
    
    old_df = test_handler.subtitles_df.copy()
    test_handler.update_subtitles_df(new_df)
    new_df = test_handler.subtitles_df

    assert len(new_df) >= len(old_df)

    old_df.to_parquet('data/subtitles.parquet', index=False)

def test_get_subtitles(test_handler):
    old_df = test_handler.subtitles_df.copy()
    test_handler.get_subtitles('shigatsu wa kimi no uso')
    intermediate_df = test_handler.subtitles_df.copy()
    test_handler.get_subtitles('ousama ranking')
    new_df = test_handler.subtitles_df

    assert (
        len(old_df) == len(intermediate_df) and
        len(new_df) >= len(intermediate_df)
    )

    old_df.to_parquet('data/subtitles.parquet', index=False)