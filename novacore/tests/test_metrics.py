from novacore.models.metrics import compute_metrics
from novacore.models.novacore import NovaCoreMini


def test_compute_metrics_basic():
    m = compute_metrics(total=4, verified=3, retries_sum=2)
    assert m.accuracy == 0.75
    assert m.avg_retries == 0.5


def test_retry_field_present_and_non_negative():
    model = NovaCoreMini(max_retries=1)
    out = model.run("STORE_COLOR C4 | SHIFT N1 | QUERY")
    assert out.retries_used >= 0
