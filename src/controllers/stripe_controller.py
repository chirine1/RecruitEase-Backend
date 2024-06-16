from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import stripe
from src.schemas.package import PaymentSchema
from src.schemas.package import PackageCreate as create_schema
from src.services.company import CompanyService
from src.services.payment import PaymentService
from decouple import config

from src.services.user import AuthService


class StripeController:
    
    def __init__(
        self,
        service: Annotated[PaymentService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        company_service: Annotated[CompanyService, Depends()],
    ) -> None:
        self.service = service
        self.auth_service = auth_service
        self.company_service= company_service

    stripe.api_key = config("STRIPE_API_KEY")

    async def create_payment(self, body:PaymentSchema):
        package = await self.service.get_one_by_unique_label(body.label)
        if not package :
            return
        try:
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=package.amount*100,
                currency='usd',
                # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JSONResponse(content={'clientSecret': intent['client_secret']})
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))
        

    async def create(self, body: create_schema):
        return await self.service.create(body)
    
    async def success(self, token:str , label:str):
        company_id = await self.auth_service.get_current_user_id(token)
        result = await self.company_service.set_package(label,company_id)
        if not result:
            return JSONResponse(
                status_code=404,
                content="package or company not found "
            )
        return JSONResponse(
            status_code=200,
            content="successfully updated compan payment details"
        )
    
    async def init_package(self):
        return await self.service.init_package()