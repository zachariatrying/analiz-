import pandas as pd
import datetime

class MacroDataManager:
    def __init__(self):
        # Static list of key economic events (FED & TCMB)
        # Source: Federal Reserve & TCMB Official Sites
        self.events = [
            # --- FED (Federal Reserve) Interest Rate Decisions ---
            # 2025 (Projected/Scheduled)
            {'date': '2025-01-29', 'event': 'FED Faiz Kararı', 'type': 'FED'},
            {'date': '2025-03-19', 'event': 'FED Faiz Kararı', 'type': 'FED'},
            # 2024
            {'date': '2024-12-18', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'}, # 4.25-4.50 range example
            {'date': '2024-11-07', 'event': 'FED Faiz İndirimi (25bp)', 'type': 'FED'},
            {'date': '2024-09-18', 'event': 'FED Faiz İndirimi (50bp)', 'type': 'FED'},
            {'date': '2024-07-31', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2024-06-12', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2024-05-01', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2024-03-20', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2024-01-31', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            # 2023
            {'date': '2023-12-13', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2023-11-01', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2023-09-20', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2023-07-26', 'event': 'FED Faiz Artışı (25bp)', 'type': 'FED'},
            {'date': '2023-06-14', 'event': 'FED Faiz Kararı (Sabit)', 'type': 'FED'},
            {'date': '2023-05-03', 'event': 'FED Faiz Artışı (25bp)', 'type': 'FED'},
            {'date': '2023-03-22', 'event': 'FED Faiz Artışı (25bp)', 'type': 'FED'},
            {'date': '2023-02-01', 'event': 'FED Faiz Artışı (25bp)', 'type': 'FED'},

            # --- TCMB (Turkey Central Bank) Interest Rate Decisions ---
            # 2025
            {'date': '2025-01-23', 'event': 'TCMB Faiz Kararı', 'type': 'TCMB'},
            # 2024
            {'date': '2024-12-26', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-11-21', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-10-17', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-09-19', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-08-22', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-07-25', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-06-27', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-05-23', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-04-25', 'event': 'TCMB Faiz Kararı (Sabit %50)', 'type': 'TCMB'},
            {'date': '2024-03-21', 'event': 'TCMB Faiz Artışı (%50)', 'type': 'TCMB'}, # 500bp hike
            {'date': '2024-02-22', 'event': 'TCMB Faiz Kararı (Sabit %45)', 'type': 'TCMB'},
            {'date': '2024-01-25', 'event': 'TCMB Faiz Artışı (%45)', 'type': 'TCMB'},
            # 2023 (Major Turns)
            {'date': '2023-12-21', 'event': 'TCMB Faiz Artışı (%42.5)', 'type': 'TCMB'},
            {'date': '2023-11-23', 'event': 'TCMB Faiz Artışı (%40)', 'type': 'TCMB'},
            {'date': '2023-10-26', 'event': 'TCMB Faiz Artışı (%35)', 'type': 'TCMB'},
            {'date': '2023-09-21', 'event': 'TCMB Faiz Artışı (%30)', 'type': 'TCMB'},
            {'date': '2023-08-24', 'event': 'TCMB Faiz Artışı (%25)', 'type': 'TCMB'}, # Massive hike
            {'date': '2023-07-20', 'event': 'TCMB Faiz Artışı (%17.5)', 'type': 'TCMB'},
            {'date': '2023-06-22', 'event': 'TCMB Faiz Artışı (%15)', 'type': 'TCMB'}, # Start of tightening cycle

            # Inflation Reports (Sample)
            {'date': '2024-01-03', 'event': 'TUİK Aralık Enflasyonu', 'type': 'Inflation'},
            {'date': '2024-02-05', 'event': 'TUİK Ocak Enflasyonu', 'type': 'Inflation'},
            {'date': '2024-03-04', 'event': 'TUİK Şubat Enflasyonu', 'type': 'Inflation'},
        ]

    def get_events_between(self, start_date, end_date):
        """Returns events that fall within the given date range."""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        filtered_events = []
        for e in self.events:
            d = pd.to_datetime(e['date'])
            if start <= d <= end:
                filtered_events.append(e)
        return filtered_events

    def get_recent_event(self, current_date, lookback_days=7):
        """Checks if a major event happened in the last N days."""
        curr = pd.to_datetime(current_date)
        start = curr - pd.Timedelta(days=lookback_days)
        
        recent = []
        for e in self.events:
            d = pd.to_datetime(e['date'])
            if start <= d <= curr:
                recent.append(e)
        return recent
