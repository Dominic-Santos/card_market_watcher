from run import main
from unittest.mock import patch

@patch('run.MarketWatcher')
def test_main(mock_market_watcher):
    main()
    mock_market_watcher.assert_called_once()
    mock_market_watcher.return_value.run.assert_called_once()
