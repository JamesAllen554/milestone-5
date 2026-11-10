import urllib.request
import re
import json
import csv
import io
import time
import sys

# Stadium metadata dictionary
STADIUM_META = {
    "American Family Field": {"team": "Brewers", "abbrev": "MIL", "league": "NL", "division": "NL Central", "city": "Milwaukee, WI", "elevation": 600, "roof": "Retractable", "color": "#0a2351"},
    "Angel Stadium": {"team": "Angels", "abbrev": "LAA", "league": "AL", "division": "AL West", "city": "Anaheim, CA", "elevation": 160, "roof": "Open", "color": "#ba0021"},
    "Busch Stadium": {"team": "Cardinals", "abbrev": "STL", "league": "NL", "division": "NL Central", "city": "St. Louis, MO", "elevation": 465, "roof": "Open", "color": "#c41e3a"},
    "Chase Field": {"team": "D-backs", "abbrev": "ARI", "league": "NL", "division": "NL West", "city": "Phoenix, AZ", "elevation": 1059, "roof": "Retractable", "color": "#a71930"},
    "Citi Field": {"team": "Mets", "abbrev": "NYM", "league": "NL", "division": "NL East", "city": "Queens, NY", "elevation": 13, "roof": "Open", "color": "#002d72"},
    "Citizens Bank Park": {"team": "Phillies", "abbrev": "PHI", "league": "NL", "division": "NL East", "city": "Philadelphia, PA", "elevation": 20, "roof": "Open", "color": "#e81828"},
    "Comerica Park": {"team": "Tigers", "abbrev": "DET", "league": "AL", "division": "AL Central", "city": "Detroit, MI", "elevation": 600, "roof": "Open", "color": "#0c2340"},
    "Coors Field": {"team": "Rockies", "abbrev": "COL", "league": "NL", "division": "NL West", "city": "Denver, CO", "elevation": 5197, "roof": "Open", "color": "#333366"},
    "Dodger Stadium": {"team": "Dodgers", "abbrev": "LAD", "league": "NL", "division": "NL West", "city": "Los Angeles, CA", "elevation": 510, "roof": "Open", "color": "#005a9c"},
    "UNIQLO Field at Dodger Stadium": {"team": "Dodgers", "abbrev": "LAD", "league": "NL", "division": "NL West", "city": "Los Angeles, CA", "elevation": 510, "roof": "Open", "color": "#005a9c"},
    "Fenway Park": {"team": "Red Sox", "abbrev": "BOS", "league": "AL", "division": "AL East", "city": "Boston, MA", "elevation": 20, "roof": "Open", "color": "#bd3039"},
    "Globe Life Field": {"team": "Rangers", "abbrev": "TEX", "league": "AL", "division": "AL West", "city": "Arlington, TX", "elevation": 550, "roof": "Retractable", "color": "#003278"},
    "Great American Ball Park": {"team": "Reds", "abbrev": "CIN", "league": "NL", "division": "NL Central", "city": "Cincinnati, OH", "elevation": 490, "roof": "Open", "color": "#c6011f"},
    "Guaranteed Rate Field": {"team": "White Sox", "abbrev": "CWS", "league": "AL", "division": "AL Central", "city": "Chicago, IL", "elevation": 595, "roof": "Open", "color": "#27251f"},
    "Kauffman Stadium": {"team": "Royals", "abbrev": "KC", "league": "AL", "division": "AL Central", "city": "Kansas City, MO", "elevation": 750, "roof": "Open", "color": "#004687"},
    "loanDepot park": {"team": "Marlins", "abbrev": "MIA", "league": "NL", "division": "NL East", "city": "Miami, FL", "elevation": 10, "roof": "Retractable", "color": "#00a3e0"},
    "Marlins Park": {"team": "Marlins", "abbrev": "MIA", "league": "NL", "division": "NL East", "city": "Miami, FL", "elevation": 10, "roof": "Retractable", "color": "#00a3e0"},
    "Minute Maid Park": {"team": "Astros", "abbrev": "HOU", "league": "AL", "division": "AL West", "city": "Houston, TX", "elevation": 50, "roof": "Retractable", "color": "#eb6e1f"},
    "Nationals Park": {"team": "Nationals", "abbrev": "WSH", "league": "NL", "division": "NL East", "city": "Washington, DC", "elevation": 25, "roof": "Open", "color": "#ab0003"},
    "Oakland Coliseum": {"team": "Athletics", "abbrev": "OAK", "league": "AL", "division": "AL West", "city": "Oakland, CA", "elevation": 10, "roof": "Open", "color": "#003831"},
    "Sutter Health Park": {"team": "Athletics", "abbrev": "OAK", "league": "AL", "division": "AL West", "city": "Sacramento, CA", "elevation": 25, "roof": "Open", "color": "#003831"},
    "Oracle Park": {"team": "Giants", "abbrev": "SF", "league": "NL", "division": "NL West", "city": "San Francisco, CA", "elevation": 11, "roof": "Open", "color": "#fd5a1e"},
    "Oriole Park at Camden Yards": {"team": "Orioles", "abbrev": "BAL", "league": "AL", "division": "AL East", "city": "Baltimore, MD", "elevation": 30, "roof": "Open", "color": "#df4601"},
    "Petco Park": {"team": "Padres", "abbrev": "SD", "league": "NL", "division": "NL West", "city": "San Diego, CA", "elevation": 15, "roof": "Open", "color": "#2f241d"},
    "PNC Park": {"team": "Pirates", "abbrev": "PIT", "league": "NL", "division": "NL Central", "city": "Pittsburgh, PA", "elevation": 725, "roof": "Open", "color": "#fdb827"},
    "Progressive Field": {"team": "Guardians", "abbrev": "CLE", "league": "AL", "division": "AL Central", "city": "Cleveland, OH", "elevation": 660, "roof": "Open", "color": "#e31937"},
    "Rogers Centre": {"team": "Blue Jays", "abbrev": "TOR", "league": "AL", "division": "AL East", "city": "Toronto, ON", "elevation": 270, "roof": "Retractable", "color": "#134a8e"},
    "T-Mobile Park": {"team": "Mariners", "abbrev": "SEA", "league": "AL", "division": "AL West", "city": "Seattle, WA", "elevation": 10, "roof": "Retractable", "color": "#0c2c56"},
    "Safeco Field": {"team": "Mariners", "abbrev": "SEA", "league": "AL", "division": "AL West", "city": "Seattle, WA", "elevation": 10, "roof": "Retractable", "color": "#0c2c56"},
    "Target Field": {"team": "Twins", "abbrev": "MIN", "league": "AL", "division": "AL Central", "city": "Minneapolis, MN", "elevation": 840, "roof": "Open", "color": "#002b5c"},
    "Tropicana Field": {"team": "Rays", "abbrev": "TB", "league": "AL", "division": "AL East", "city": "St. Petersburg, FL", "elevation": 45, "roof": "Fixed Dome", "color": "#092c5c"},
    "Truist Park": {"team": "Braves", "abbrev": "ATL", "league": "NL", "division": "NL East", "city": "Atlanta, GA", "elevation": 980, "roof": "Open", "color": "#ce1141"},
    "SunTrust Park": {"team": "Braves", "abbrev": "ATL", "league": "NL", "division": "NL East", "city": "Atlanta, GA", "elevation": 980, "roof": "Open", "color": "#ce1141"},
    "Wrigley Field": {"team": "Cubs", "abbrev": "CHC", "league": "NL", "division": "NL Central", "city": "Chicago, IL", "elevation": 600, "roof": "Open", "color": "#0e3386"},
    "Yankee Stadium": {"team": "Yankees", "abbrev": "NYY", "league": "AL", "division": "AL East", "city": "Bronx, NY", "elevation": 54, "roof": "Open", "color": "#003087"}
}

# Team code map to stadium name
TEAM_TO_STADIUM = {
    "MIL": "American Family Field",
    "LAA": "Angel Stadium",
    "STL": "Busch Stadium",
    "ARI": "Chase Field",
    "NYM": "Citi Field",
    "PHI": "Citizens Bank Park",
    "DET": "Comerica Park",
    "COL": "Coors Field",
    "LAD": "Dodger Stadium",
    "BOS": "Fenway Park",
    "TEX": "Globe Life Field",
    "CIN": "Great American Ball Park",
    "CWS": "Guaranteed Rate Field",
    "KC": "Kauffman Stadium",
    "MIA": "loanDepot park",
    "HOU": "Minute Maid Park",
    "WSH": "Nationals Park",
    "OAK": "Oakland Coliseum",
    "SF": "Oracle Park",
    "BAL": "Oriole Park at Camden Yards",
    "SD": "Petco Park",
    "PIT": "PNC Park",
    "CLE": "Progressive Field",
    "TOR": "Rogers Centre",
    "SEA": "T-Mobile Park",
    "MIN": "Target Field",
    "TB": "Tropicana Field",
    "ATL": "Truist Park",
    "CHC": "Wrigley Field",
    "NYY": "Yankee Stadium"
}

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8')
        m = re.search(r'var data = (\[.*?\]);', html)
        if m:
            return json.loads(m.group(1))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return []

def main():
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    splits = ["", "L", "R"]  # "" means All

    print("--- 1. Fetching Dimensions Data ---")
    dims_by_year = {}
    for y in years:
        url = f"https://baseballsavant.mlb.com/leaderboard/statcast-park-factors?type=dimensions&year={y}"
        data = fetch_json(url)
        dims_by_year[y] = {str(d['venue_id']): d for d in data}
        print(f"Year {y}: {len(data)} venues dimensions")

    print("\n--- 2. Fetching Park Factors Data ---")
    park_factor_records = []

    for y in years:
        for split in splits:
            split_label = "All" if split == "" else ("LHB" if split == "L" else "RHB")
            url = f"https://baseballsavant.mlb.com/leaderboard/statcast-park-factors?year={y}&batSide={split}&stat=index_woba&condition=All&rolling=1"
            pf_data = fetch_json(url)
            print(f"Year {y} Split {split_label}: {len(pf_data)} venues")
            dims = dims_by_year.get(y, {})

            for pf in pf_data:
                vid = str(pf.get('venue_id'))
                venue_name = pf.get('venue_name', '')
                club = pf.get('name_display_club', '')

                # Match with dimensions
                dim = dims.get(vid)
                if not dim:
                    # Try matching by name
                    for d in dims.values():
                        if d.get('name_display_club') == club or d.get('venue_name_short') == venue_name:
                            dim = d
                            break

                # Metadata
                norm_name = venue_name
                if "Dodger Stadium" in venue_name:
                    norm_name = "Dodger Stadium"
                meta = STADIUM_META.get(norm_name, STADIUM_META.get(venue_name, {}))

                record = {
                    "venue_id": vid,
                    "venue_name": venue_name,
                    "team": meta.get("team", club),
                    "abbrev": meta.get("abbrev", ""),
                    "league": meta.get("league", "MLB"),
                    "division": meta.get("division", "MLB"),
                    "city": meta.get("city", ""),
                    "elevation": meta.get("elevation", 0),
                    "roof": meta.get("roof", "Open"),
                    "color": meta.get("color", "#1d4ed8"),
                    "season": y,
                    "split": split_label,
                    "pa": int(pf.get('n_pa', 0)) if pf.get('n_pa') else 0,
                    # Park factors (100 = average)
                    "index_hr": int(pf.get('index_hr', 100)) if pf.get('index_hr') else 100,
                    "index_runs": int(pf.get('index_runs', 100)) if pf.get('index_runs') else 100,
                    "index_hardhit": int(pf.get('index_hardhit', 100)) if pf.get('index_hardhit') else 100,
                    "index_hits": int(pf.get('index_hits', 100)) if pf.get('index_hits') else 100,
                    "index_1b": int(pf.get('index_1b', 100)) if pf.get('index_1b') else 100,
                    "index_2b": int(pf.get('index_2b', 100)) if pf.get('index_2b') else 100,
                    "index_3b": int(pf.get('index_3b', 100)) if pf.get('index_3b') else 100,
                    "index_woba": int(pf.get('index_woba', 100)) if pf.get('index_woba') else 100,
                }

                if dim:
                    record["distance_lf_line"] = round(float(dim.get('distance_lf_line', 0)), 1)
                    record["distance_lf_gap"] = round(float(dim.get('distance_lf_gap', 0)), 1)
                    record["distance_cf"] = round(float(dim.get('distance_cf', 0)), 1)
                    record["distance_rf_gap"] = round(float(dim.get('distance_rf_gap', 0)), 1)
                    record["distance_rf_line"] = round(float(dim.get('distance_rf_line', 0)), 1)
                    record["distance_deepest"] = round(float(dim.get('distance_deepest', 0)), 1)
                    record["height_lf_line"] = round(float(dim.get('height_lf_line', 0)), 1)
                    record["height_highest"] = round(float(dim.get('height_highest', 0)), 1)
                    record["avg_fence_distance"] = round(float(dim.get('avg_fence_distance', 0)), 1)
                    record["avg_hr_distance"] = round(float(dim.get('avg_hr_distance', 0)), 1)
                    record["fence_area"] = round(float(dim.get('fence_area', 0)), 0)
                    record["avg_fence_height"] = round(float(dim.get('avg_fence_height', 0)), 1)
                else:
                    record["distance_lf_line"] = 330
                    record["distance_lf_gap"] = 375
                    record["distance_cf"] = 400
                    record["distance_rf_gap"] = 375
                    record["distance_rf_line"] = 330
                    record["distance_deepest"] = 405
                    record["height_lf_line"] = 8
                    record["height_highest"] = 10
                    record["avg_fence_distance"] = 370
                    record["avg_hr_distance"] = 398
                    record["fence_area"] = 110000
                    record["avg_fence_height"] = 8

                park_factor_records.append(record)
            time.sleep(0.1)

    print(f"Total Park Dimension & Factor records: {len(park_factor_records)}")

    print("\n--- 3. Fetching Statcast Home Runs ---")
    # Fetch 3500+ home runs from 2024
    hr_url = 'https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=home%5C.%5C.run%7C&hfGT=R%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C&hfSit=&player_type=batter&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&team=&home_road=&hfRO=&flag_is_reverse=&hfFlag=&hfRate=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc&min_abs=0&type=details'
    
    req = urllib.request.Request(hr_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    homeruns = []
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            reader = csv.DictReader(io.TextIOWrapper(resp, encoding='utf-8', errors='ignore'))
            for row in reader:
                try:
                    ev = float(row.get('launch_speed', 0))
                    la = float(row.get('launch_angle', 0))
                    dist = float(row.get('hit_distance_sc', 0))
                    team_abbrev = row.get('home_team', '')
                    if ev > 80 and dist > 250 and team_abbrev:
                        stadium = TEAM_TO_STADIUM.get(team_abbrev, team_abbrev)
                        meta = STADIUM_META.get(stadium, {})
                        homeruns.append({
                            "player": row.get('player_name', 'Unknown'),
                            "date": row.get('game_date', ''),
                            "team": team_abbrev,
                            "stadium": stadium,
                            "ev": round(ev, 1),
                            "la": round(la, 1),
                            "dist": round(dist, 1),
                            "stand": row.get('stand', ''),
                            "pitch_speed": round(float(row.get('release_speed', 0)), 1) if row.get('release_speed') else None,
                            "color": meta.get('color', '#3b82f6'),
                            "league": meta.get('league', 'MLB'),
                            "des": row.get('des', '')
                        })
                except (ValueError, TypeError):
                    continue
                if len(homeruns) >= 3500:
                    break
        print(f"Successfully collected {len(homeruns)} individual home runs!")
    except Exception as e:
        print(f"Error fetching HRs: {e}")

    # Save to data directory
    import os
    os.makedirs("data", exist_ok=True)
    with open("data/park_dimensions_factors.json", "w") as f:
        json.dump(park_factor_records, f)
    with open("data/statcast_homeruns.json", "w") as f:
        json.dump(homeruns, f)

    print("Data files saved successfully!")

if __name__ == "__main__":
    main()