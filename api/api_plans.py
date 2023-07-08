from fastapi import APIRouter, Depends, HTTPException
import mongo.functions.plan_functions as plan_functions
import mongo.models.plan_model as plan_model
from .api_auth import authorize_token, check_permission
from typing import Optional

router_plan = APIRouter(
    prefix="/plan",
    tags=["Plan"],
    responses={404: {"description": "Not found"}},
)

@router_plan.post("/")
async def insert_new_plan(plan: plan_model.Plan, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        plan = plan_model.Plan(**plan.dict())
        if plan_functions.create_plan(plan):
            return {"status": "Plan created"}
        else:
            raise HTTPException(status_code=400, detail="Plan already exists")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_plan.get("/")
async def get_plan(id_or_plan: str, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_plan:
            plan = plan_functions.get_plan(id_or_plan)
            if plan:
                return plan
            else:
                raise HTTPException(status_code=400, detail="Plan not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_plan.put("/")
async def update_plan(id_or_plan: str, plan: plan_model.Plan.Update = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_plan:
            if plan_functions.update_plan(plan, id_or_plan):
                return {"status": "Plan updated"}
            else:
                raise HTTPException(status_code=400, detail="Plan not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
        
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_plan.delete("/")
async def delete_plan(id_or_plan: str, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_plan:
            if plan_functions.delete_plan(id_or_plan):
                return {"status": "Plan deleted"}
            else:
                raise HTTPException(status_code=400, detail="Plan not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_plan.get("/all/")
async def get_all_plans(authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        plans = plan_functions.get_all_plans()
        plans = [plan for plan in plans]
        if plans:
            return plans
        else:
            raise HTTPException(status_code=400, detail="No plans found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_plan.put("/add/resource/")
async def add_resource_to_plan(id_or_plan: str, resource: plan_model.Plan.UpdateResources = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_plan:
            if plan_functions.add_resource_to_plan(id_or_plan, resource):
                return {"status": "Resource added to plan"}
            else:
                raise HTTPException(status_code=400, detail="Plan not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_plan.put("/update/resource/")
async def update_resource_from_plan(id_or_plan: str, resource: plan_model.Plan.UpdateResources = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_plan:
            if plan_functions.update_resource_from_plan(id_or_plan, resource):
                return {"status": "Resource updated from plan"}
            else:
                raise HTTPException(status_code=400, detail="Plan not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    