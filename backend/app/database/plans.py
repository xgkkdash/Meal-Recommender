from app.schemas import Plan


async def insert_plan(db, plan: Plan):
    doc = await db.plans.insert_one(plan.dict())
    return doc


async def find_plan(db, user_id, plan_id):
    doc = await db.plans.find_one({"user_id": user_id, "plan_id": plan_id})
    if doc:
        doc.pop("_id", None)
    return Plan(**doc) if doc else None


async def find_user_plans(db, user_id):
    docs = [doc async for doc in db.plans.find({"user_id": user_id})]
    for doc in docs:
        doc.pop("_id", None)
    plans = [Plan(**doc) for doc in docs]
    return plans


async def delete_plan(db, user_id, plan_id):
    result = await db.plans.delete_many({"user_id": user_id, "plan_id": plan_id})
    return result


async def drop_plans(db):
    result = await db.plans.drop()
    return result
