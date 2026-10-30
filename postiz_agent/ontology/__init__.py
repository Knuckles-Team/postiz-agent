"""Social & Content ontology contribution (CONCEPT:AU-KG.ontology.package-federation-migration).

Data-only subpackage: it carries ``social.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/social`` module — social media, content creation and
audience engagement bridging Postiz, Owncast and social network analytics, with
both time-series engagement observations and aggregated snapshots) which the
scion-sdk hub federates in via the ``scion_sdk.ontology_providers``
entry-point. It holds no business logic and no heavy imports so the hub can
resolve it cheaply.
"""
