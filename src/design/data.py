_PASS = "Pass"
_FAIL = "Fail"
_N_A = "N/A"
_NO = "No"
_YES = "Yes"
_ONE = "1"
_ZERO = "0"
_SPACE = " "


class ScriptTest:
    def __init__(self, name: str, *options: str):
        self.name = name
        self.options = options


_CASTORS_Y = ScriptTest("CASTORS", _PASS, _N_A, _FAIL)
_FRAME = ScriptTest("FRAME", _PASS, _FAIL, _N_A)
_PAINT = ScriptTest("PAINT", _PASS, _FAIL, _N_A)
_LABELLING = ScriptTest("LABELLING", _PASS, _FAIL, _N_A)
_CHARGER_N = ScriptTest("CHARGER", _N_A, _PASS, _FAIL)
_BATTERY_N = ScriptTest("BATTERY", _N_A, _PASS, _FAIL)
_BATTERY_Y = ScriptTest("BATTERY", _PASS, _N_A, _FAIL)
_CONTROL = ScriptTest("CONTROL", _PASS, _FAIL, _N_A)
_CONDITION = ScriptTest("CONDITION", _ONE, _ZERO)
_FURTHER_ATTENTION = ScriptTest("FURTHER_ATTENTION", _NO, _YES)
_DETAILS = ScriptTest("DETAILS", _PASS, _N_A, _FAIL)
_GENERAL_WEAR = ScriptTest("GENERAL WEAR", _PASS, _N_A, _FAIL)
_STITCHING = ScriptTest("STITCHING", _PASS, _N_A, _FAIL)
_FITTINGS = ScriptTest("FITTINGS", _PASS, _N_A, _FAIL)
_VELCRO_N = ScriptTest("VELCRO", _N_A, _PASS, _FAIL)
_HARDWARE = ScriptTest("HARDWARE", _PASS, _N_A, _FAIL)
_OPERATION = ScriptTest("OPERATION", _PASS, _N_A, _FAIL)
_ATTACHMENTS = ScriptTest("ATTACHMENTS", _N_A, _PASS, _FAIL)
_STRAP = ScriptTest("STRAP", _PASS, _N_A, _FAIL)
_ROLLERS = ScriptTest("ROLLERS", _PASS, _N_A, _FAIL)
_MOTORS = ScriptTest("MOTORS", _PASS, _N_A, _FAIL)
_CHARGING_CONTACTS = ScriptTest("CHARGING CONTACTS", _PASS, _N_A, _FAIL)
_STATUS_LEDS = ScriptTest("STATUS LEDS", _PASS, _N_A, _FAIL)
_END_LIMIT = ScriptTest("END LIMIT", _PASS, _N_A, _FAIL)
_SLING_INSPECTION = ScriptTest("SLING INSPECTION", _N_A, _PASS, _FAIL)
_LOAD_TEST = ScriptTest("LOAD TEST", _PASS, _N_A, _FAIL)
_EMERGENCY_OFF = ScriptTest("EMERGENCY OFF", _PASS, _N_A, _FAIL)
_MECHANICAL_LOWERING = ScriptTest("MECHANICAL LOWERING", _PASS, _N_A, _FAIL)
_ELECTRICAL_LOWERING = ScriptTest("ELECTRICAL LOWERING", _PASS, _N_A, _FAIL)
_ELECTRICAL_LIFTING = ScriptTest("ELECTRICAL LIFTING", _PASS, _N_A, _FAIL)
_RESET = ScriptTest("RESET", _N_A, _PASS, _FAIL)
_NUMBER_OF_LIFTS = ScriptTest("NUMBER OF LIFTS")
_USAGE_ENVIRONMENT = ScriptTest("USAGE ENVIRONMENT", _NO, _YES)
_FEATURES = ScriptTest("FEATURES", _PASS, _N_A, _FAIL)
_TRACK_DUST = ScriptTest("TRACK DUST", _PASS, _N_A, _FAIL)
_TRACK_LOAD_KG = ScriptTest("TRACK LOAD TEST", "150")
_ELECTRIC_TEST = ScriptTest("ELECTRIC TEST", _N_A, _PASS, _FAIL)
_HELP_POLE = ScriptTest("HELP POLE", _N_A, _PASS, _FAIL)
_VISUAL = ScriptTest("VISUAL", _PASS, _N_A, _FAIL)
_PIVOTS = ScriptTest("PIVOTS", _PASS, _N_A, _FAIL)
_SWIVEL = ScriptTest("SWIVEL", _PASS, _N_A, _FAIL)
_ACCURACY = ScriptTest("ACCURACY", _PASS, _N_A, _FAIL)
_SEAT_FUNCTIONS = ScriptTest("SEAT FUNCTIONS", _PASS, _N_A, _FAIL)
_ELECTRIC_N = ScriptTest("ELECTRIC", _N_A, _PASS, _FAIL)
_CAPACITY = ScriptTest("CAPACITY", _PASS, _N_A, _FAIL)
_DATE = ScriptTest("DATE", _PASS, _N_A, _FAIL)
_MAINS = ScriptTest("MAINS", _PASS, _N_A, _FAIL)
_FUSES = ScriptTest("FUSES", _PASS, _N_A, _FAIL)
_EARTH_RESISTANCE = ScriptTest("EARTH RESISTANCE", _SPACE)
_INSULATION_RESISTANCE = ScriptTest("INSULATION RESISTANCE", "199")
_INSULATION_RESISTANCE_ENCLOSURE = ScriptTest("INSULATION RESISTANCE ENCLOSURE", "199")
_TOUCH_CURRENT = ScriptTest("TOUCH CURRENT", _SPACE)
_IEC_MAINS_LEAD = ScriptTest("IEC MAINS LEAD")
_MISSING_COMPONENTS = ScriptTest("MISSING COMPONENTS", _NO, _YES)
_POLES = ScriptTest("POLES", _PASS, _N_A, _FAIL)
_CLEAN = ScriptTest("CLEAN", _PASS, _N_A, _FAIL)
_PERFORMANCE = ScriptTest("PERFORMANCE", _PASS, _N_A, _FAIL)


class Script:
    def __init__(self, nickname: str, name: str, *tests: ScriptTest, extra_terms: list[str] | None = None) -> None:
        self.nickname = nickname
        self.name = name
        self.tests = tests
        self.search_terms = extra_terms or []
        self.search_terms.append(nickname)

    def matches(self, search: str) -> bool:
        return any(term in search for term in self.search_terms)


SCRIPTS: dict[str, Script] = {
    "CHANGE TILT TABLE": Script(
        "CHANGE TILT TABLE", "AT - CHANGE / TILT TABLE, ELECTRIC/MANUAL", _CASTORS_Y, _FRAME, _PAINT, _LABELLING, _CHARGER_N, _BATTERY_N, _CONTROL, _CONDITION, _FURTHER_ATTENTION
    ),
    "SLING": Script("SLING", "AT - SLING", _DETAILS, _GENERAL_WEAR, _STITCHING, _FITTINGS, _VELCRO_N, _LABELLING, _CONDITION),
    "WALKER": Script(
        "WALKER",
        "AT - WALKER / STANDER",
        _CASTORS_Y,
        _CASTORS_Y,
        _CASTORS_Y,
        _FRAME,
        _HARDWARE,
        _PAINT,
        _OPERATION,
        _ATTACHMENTS,
        _LABELLING,
        _CONDITION,
        _FURTHER_ATTENTION,
        extra_terms=["WALK", "STAND", "STEDY"],
    ),
    "CEILING HOIST": Script(
        "CEILING",
        "AT - CEILING HOIST",
        _OPERATION,
        _CONTROL,
        _STRAP,
        _ROLLERS,
        _MOTORS,
        _CHARGER_N,
        _BATTERY_N,
        _CHARGING_CONTACTS,
        _STATUS_LEDS,
        _END_LIMIT,
        _LABELLING,
        _HARDWARE,
        _SLING_INSPECTION,
        _LOAD_TEST,
        _EMERGENCY_OFF,
        _MECHANICAL_LOWERING,
        _ELECTRICAL_LOWERING,
        _RESET,
        _NUMBER_OF_LIFTS,
        _CONDITION,
        _USAGE_ENVIRONMENT,
    ),
    "TRACK": Script("TRACK", "AT - TRACK", _FEATURES, _TRACK_DUST, _CHARGER_N, _TRACK_LOAD_KG, _LOAD_TEST, _ELECTRIC_TEST),
    "COMMODE": Script("COMMODE", "AT - COMMODE", _CASTORS_Y, _FRAME, _PAINT, _OPERATION, _LABELLING, _CHARGER_N, _BATTERY_N, _CONTROL, _CONDITION),
    "BED": Script("BED", "AT - ELECTRIC BED", _CASTORS_Y, _FRAME, _HARDWARE, _CONTROL, _PAINT, _OPERATION, _LABELLING, _CHARGER_N, _HELP_POLE, _CONDITION),
    "FLOOR HOIST": Script(
        "FLOOR",
        "AT - FLOOR HOIST",
        _CASTORS_Y,
        _VISUAL,
        _PIVOTS,
        _PAINT,
        _OPERATION,
        _HARDWARE,
        _CHARGER_N,
        _BATTERY_N,
        _CONTROL,
        _SWIVEL,
        _LOAD_TEST,
        _EMERGENCY_OFF,
        _MECHANICAL_LOWERING,
        _ELECTRICAL_LOWERING,
        _ELECTRICAL_LIFTING,
        _RESET,
        _CONDITION,
        _USAGE_ENVIRONMENT,
        extra_terms=["LIFTS"],
    ),
    "TUB": Script("TUB", "AT - TUB / BATH CHAIRS", _CASTORS_Y, _FRAME, _PAINT, _OPERATION, _LABELLING, _CHARGER_N, _BATTERY_N, _CONTROL, _CONDITION, extra_terms=["BATH"]),
    "SCALE": Script("SCALE", "AT - WEIGH CHAIR / SCALE", _CASTORS_Y, _FRAME, _PAINT, _OPERATION, _LABELLING, _CHARGER_N, _BATTERY_Y, _ACCURACY, _CONDITION, extra_terms=["WEIGH"]),
    "WHEELCHAIR": Script(
        "WHEELCHAIR",
        "AT - WHEELCHAIR",
        _CASTORS_Y,
        _CASTORS_Y,
        _CASTORS_Y,
        _CASTORS_Y,
        _CASTORS_Y,
        _PAINT,
        _FRAME,
        _FRAME,
        _HARDWARE,
        _ATTACHMENTS,
        _PAINT,
        _SEAT_FUNCTIONS,
        _OPERATION,
        _OPERATION,
        _ATTACHMENTS,
        _LABELLING,
        _CHARGER_N,
        _BATTERY_N,
        _ELECTRIC_N,
        _ELECTRIC_N,
        _CONDITION,
    ),
    "CHARGER": Script("CHARGER", "BATTERY OPERATED / VISUAL TEST", _BATTERY_N, _CONTROL, _VISUAL, _ATTACHMENTS),
    "BATTERY": Script("BATTERY", "BATTER PACK", _VISUAL, _CAPACITY, _DATE),
    "CLASS II": Script(
        "CLASS II",
        "CLASS II NO APPLIED PARTS",
        _MAINS,
        _FUSES,
        _CONTROL,
        _BATTERY_N,
        _VISUAL,
        _ATTACHMENTS,
        _EARTH_RESISTANCE,
        _INSULATION_RESISTANCE,
        _INSULATION_RESISTANCE_ENCLOSURE,
        _TOUCH_CURRENT,
        _IEC_MAINS_LEAD,
    ),
    "FURNITURE": Script(
        "FURNITURE", "FURNITURE GENERIC", _CONDITION, _CASTORS_Y, _CASTORS_Y, _PAINT, _CASTORS_Y, _MISSING_COMPONENTS, _POLES, _CLEAN, _ELECTRIC_N, _PERFORMANCE, extra_terms=["OVERBED"]
    ),
}
