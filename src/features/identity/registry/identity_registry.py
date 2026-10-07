from __future__ import annotations

from uuid import uuid4

from src.features.configuration.models import Profile

from ..models.identity import Identity

IDENTITIES_FALLBACK: tuple[Identity, ...] = (
    Identity(
        id=uuid4().__str__(),
        name='Gerardo Moraga Gajardo',
        email='gmoraga.glo@aminerals.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Josefa Andrea Parra Videla',
        email='jparravi@pelambres.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Maria Jesus Campos Andrade',
        email='mcamposa@pelambres.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Sofía Andrea Barrientos Rebolledo',
        email='sbarrientos.glo@aminerals.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Carlos Alejandro Loyola Pino',
        email='glocloyola@eeccmlp.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Fernanda Macarena Quinteros Beltran',
        email='fquinteros@pelambres.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
    Identity(
        id=uuid4().__str__(),
        name='Carolina Espinoza',
        email='cespinoza.acc@aminerals.cl',
        profile=Profile.ADMINISTRADOR.value,
        is_active=True,
    ),
)
