import urllib.request
import json
from decimal import Decimal
from typing import Dict
from typing import Any


class LiveCurrencyService:
    """Provides foreign exchange rates with an offline fallback mechanism."""

    @staticmethod
    def get_usd_rates() -> Dict[str, Decimal]:
        """Fetches the latest rates against USD. Falls back safely if the connection fails."""
        # Using a reliable open API endpoint for live corporate conversions
        url = "https://er-api.com"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NexusERP-Engine"})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                if data.get("result") == "success":
                    rates: Dict[str, Any] = data.get("rates", {})
                    return {k: Decimal(str(v)) for k, v in rates.items()}
        except Exception:
            pass  # Fall back to safe offline static parameters if the API is down

        # Offline fallbacks to maintain system stability
        return {
            "USD": Decimal("1.000000"),
            "EUR": Decimal("0.925000"),
            "GBP": Decimal("0.785000"),
            "UGX": Decimal("3750.000000"),
        }
