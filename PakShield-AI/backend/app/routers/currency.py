from fastapi import APIRouter

router = APIRouter(prefix="/api/currency", tags=["Currency"])

TIMELINE_DATA = [
    {"year": 1947, "event": "Pakistan adopted Indian Rupee with Pakistan overprints", "type": "milestone"},
    {"year": 1948, "event": "First Pakistani coins issued", "type": "milestone"},
    {"year": 1949, "event": "First Pakistan Rupee notes issued (Re.1, Rs.5, Rs.10, Rs.100)", "type": "milestone"},
    {"year": 1957, "event": "Decimal system introduced – 1 Rupee = 100 Paisa", "type": "change"},
    {"year": 1961, "event": "State Bank of Pakistan takes full control of note issuance", "type": "change"},
    {"year": 1971, "event": "War era notes with special markings issued", "type": "event"},
    {"year": 1986, "event": "Rs.50 note introduced", "type": "new_denomination"},
    {"year": 1997, "event": "Rs.5000 note introduced – highest denomination", "type": "new_denomination"},
    {"year": 2003, "event": "Enhanced security features added to Rs.1000 note", "type": "security_upgrade"},
    {"year": 2006, "event": "New series launched with advanced security features", "type": "redesign"},
    {"year": 2008, "event": "Rs.20 note introduced", "type": "new_denomination"},
    {"year": 2012, "event": "Polymer substrate trials for Rs.20 note", "type": "innovation"},
    {"year": 2020, "event": "Revised Rs.75 commemorative note issued", "type": "commemorative"},
    {"year": 2022, "event": "New security thread and watermark enhancements across all denominations", "type": "security_upgrade"},
    {"year": 2024, "event": "Digital currency pilot and advanced anti-counterfeit features", "type": "innovation"},
]

DENOMINATIONS_DATA = [
    {
        "denomination": "Rs. 5000",
        "color": "Dark Green",
        "front": "Quaid-e-Azam M.A. Jinnah",
        "back": "Faisal Mosque, Islamabad",
        "security_thread": "Green color-shifting",
        "issued": 1997,
    },
    {
        "denomination": "Rs. 1000",
        "color": "Dark Blue/Purple",
        "front": "Quaid-e-Azam M.A. Jinnah",
        "back": "Islamia College, Peshawar",
        "security_thread": "Green color-shifting",
        "issued": 1987,
    },
    {
        "denomination": "Rs. 500",
        "color": "Golden/Brown",
        "front": "Quaid-e-Azam M.A. Jinnah",
        "back": "Karakoram Highway",
        "security_thread": "Metallic",
        "issued": 2006,
    },
    {
        "denomination": "Rs. 100",
        "color": "Red/Green",
        "front": "Quaid-e-Azam M.A. Jinnah",
        "back": "Quaid-e-Azam Residency, Ziarat",
        "security_thread": "Metallic",
        "issued": 2006,
    },
    {
        "denomination": "Rs. 50",
        "color": "Purple/Green",
        "front": "Quaid-e-Azam M.A. Jinnah",
        "back": "K2 Mountain",
        "security_thread": "Metallic",
        "issued": 2006,
    },
]

EXCHANGE_RATES_DATA = {
    "USD_PKR": {"rate": 278.45, "change": 0.12, "direction": "up"},
    "EUR_PKR": {"rate": 302.15, "change": 0.21, "direction": "up"},
    "GBP_PKR": {"rate": 351.20, "change": 0.08, "direction": "up"},
    "AED_PKR": {"rate": 75.82, "change": -0.04, "direction": "down"},
    "SAR_PKR": {"rate": 74.24, "change": 0.00, "direction": "flat"},
    "CNY_PKR": {"rate": 38.45, "change": -0.15, "direction": "down"},
}


@router.get("/timeline")
async def get_timeline():
    return {"events": TIMELINE_DATA, "total": len(TIMELINE_DATA)}


@router.get("/denominations")
async def get_denominations():
    return {"denominations": DENOMINATIONS_DATA, "total": len(DENOMINATIONS_DATA)}


@router.get("/rates")
async def get_exchange_rates():
    return {"rates": EXCHANGE_RATES_DATA, "base": "PKR", "last_updated": "2026-05-15T00:00:00Z"}
