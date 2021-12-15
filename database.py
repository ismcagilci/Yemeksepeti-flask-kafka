



def get_all(model):
    data = model.query.all()
    return data


def add_instance(model,db, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    db.session.commit()
    return instance.id

def delete_instance(model,db, id):
    model.query.filter_by(id=id).delete()
    db.session.commit()

def delete_all(model,db):
    db.session.query(model).delete()
    db.session.commit()

def edit_instance(model, id,db, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    db.session.commit()

