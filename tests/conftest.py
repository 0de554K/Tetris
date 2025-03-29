import pytest
import pygame as pg

@pytest.fixture(scope='module')
def pg_init():
    pg.init()
    yield
    pg.quit()


@pytest.fixture
def dummy_app():
    class DummyApp:
        def __init__(self):
            self.anim_trigger = True
            self.fast_anim_trigger = False
            self.images = [pg.Surface((10, 10))]
            self.screen = pg.Surface((800, 600))
    return DummyApp()

@pytest.fixture
def dummy_tetris():
    class DummyTetris:
        def __init__(self, shape='T'):
            self.tetromino = type('Tetromino', (), {'shape': shape})
    return DummyTetris()