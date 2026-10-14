"""Pure unit tests; stub Cog because these tests don't start Docker."""
import sys
import types
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

class _DummyInput:
    def __init__(self, **kwargs):
        self.default = kwargs.get('default')
        self.choices = kwargs.get('choices')
        self.description = kwargs.get('description')

mock_cog = types.ModuleType('cog')
mock_cog.BasePredictor = type('BasePredictor', (), {})
mock_cog.Path = Path
mock_cog.Secret = type('Secret', (), {})
mock_cog.Input = _DummyInput
sys.modules.setdefault('cog', mock_cog)

from predict import build_arguments, Predictor


def test_auto_duration_is_sent_as_auto():
    args = build_arguments('Test', 'Auto', '16:9', True, ['img'], [])
    assert args['duration'] == 'auto'
    assert args['resolution'] == '720p'
    assert args['image_urls'] == ['img']


def test_fixed_thirty():
    assert build_arguments('Test', '30', '9:16', False, [], [])['duration'] == '30'


def test_no_480p():
    import inspect
    duration = inspect.signature(Predictor.predict).parameters['duration'].default
    assert 'Auto' in duration.choices
    assert duration.default == 'Auto'
    assert '480p' not in build_arguments('Test', 'Auto', '16:9', True, [], {}).values()
