from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.write_concern import WriteConcern


def mongo_client():
    if not settings.MONGODB_URI:
        raise ImproperlyConfigured('MONGODB_URI no está configurada.')
    return MongoClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000,
        tz_aware=True,
    )


def deliver_event(event):
    """Usa el UUID como _id para permitir reintentos sin duplicar el log."""
    document = {
        '_id': str(event.event_id),
        'event_id': str(event.event_id),
        'broker_id': event.broker_id,
        'user_id': event.actor_id,
        'occurred_at': event.occurred_at,
        'action': event.action,
        'record_id': event.record_id,
        'source': event.source,
        'changes': event.changes,
    }
    with mongo_client() as client:
        collection = client[settings.MONGODB_DATABASE]['auditoria'].with_options(
            write_concern=WriteConcern(w='majority', wtimeout=5000)
        )
        result = collection.update_one({'_id': document['_id']}, {'$setOnInsert': document}, upsert=True)
        if not result.acknowledged:
            raise PyMongoError('La escritura no fue confirmada; conservar el evento pendiente.')
