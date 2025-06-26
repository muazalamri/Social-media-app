from .__init__ import db
from .classes import *
# Utility functions
def add_to_db(model, **kwargs):
    new_item = model(**kwargs)
    db.session.add(new_item)
    db.session.commit()
    return new_item.id

def load_data(model, id=None, filter=None, limit=None, exists_field=None, exists_value=None, sql_text=None, entities=None, case=None, order_by=None,start_date=None,end_date=None):
    query = db.session.query(model)
    if start_date is not None:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()

        # Query for events in this range
        query = query.filter(
            func.date(Event.created_at) >= start
        )
    if end_date is not None:
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Query for events in this range
        query = query.filter(
            func.date(Event.created_at) <= end
        )

    if id is not None:
        query = query.filter(model.id == id)

    if order_by is not None:
        query.order_by(order_by)

    if filter is not None:
        query = query.filter(filter)

    if limit is not None:
        query = query.limit(limit)

    if exists_field is not None and exists_value is not None:
        query = query.filter(getattr(model, exists_field) == exists_value)

    if sql_text is not None:
        query = query.filter(db.text(sql_text))

    if entities is not None:
        query = query.with_entities(*entities)

    if case is not None:
        query = query.filter(model.some_field.ilike(case) if case else model.some_field.like(case))

    return query.all()
def appender(fatherModel,model,fatherElementId:int,elementIds:list,propertyName:str):
    fatherElement=load_data(fatherModel,id=fatherElementId)
    for element in elementIds:
        getattr(fatherElement,propertyName).append(load_data(model,id=element))
    db.session.commit()
def remover(fatherModel,model,fatherElementId:int,elementId:int,propertyName:str):
    fatherElement=load_data(fatherModel,id=fatherElementId)
    fatherElement.remove(load_data(model,id=elementId))
    db.session.commit()
def setData(model,id,kwargs):
    element=load_data(model,id=id)
    for key in kwargs:
        setattr(element,key,kwargs[key])
    db.session.commit()
def add_form(model,*filds:list[str], **kwargs:dict[str]):
    kwargs={f'{fild}':typer(kwargs[f'{fild}']) for fild in filds}
    new_item = model(**kwargs)
    db.session.add(new_item)
    db.session.commit()
def typer(data):
    if type(data) in [str,int]:
        return data
    return str(data)