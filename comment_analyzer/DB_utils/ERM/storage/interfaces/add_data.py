
from ....ERM.storage.interfaces.upsert import UpsertInterface
from ....ERM.storage.results.analyze_res import AnalyzerResult


UPSERT = UpsertInterface()


def add_analyze(comment_id, vendor_id, comment_text, vendor_code, qualities, services, overall, foods):
    obj = AnalyzerResult(
        comment_id=comment_id,
        vendor_id=vendor_id,
        comment_text=comment_text,
        vendor_code=vendor_code,
        qualities=qualities,
        services=services,
        overall=overall,
        foods=foods)
    UPSERT.write([obj])
    UPSERT.clos()
