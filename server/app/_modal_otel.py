import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.settings import settings

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = settings.MODAL_OTEL_EXPORTER_OTLP_ENDPOINT
os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = settings.MODAL_OTEL_EXPORTER_OTLP_INSECURE
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = settings.MODAL_OTEL_EXPORTER_OTLP_PROTOCOL

provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter()
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
