from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
import json
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.db')    
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Modules
db = SQLAlchemy(app)

# Models
class Indicator(db.Model):
    __tablename__ = 'indicators'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(256), index=True)
    category = db.Column(db.String(256), index=True)
    indicator = db.Column(db.String(256), index=True)
    unit = db.Column(db.String(256), index=True)
    
    def __repr__(self):
        return '<method %r>' % self.method

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(256), index=True, unique=True)
    unit = db.Column(db.String(256), index=True)
    impacts = db.relationship('Impact',  uselist=True, backref='method')
    geography_id = db.Column(db.String(255), db.ForeignKey('geographies.id'))

    
    def __repr__(self):
        return '<product_name %r>' % self.product_name

class Impact(db.Model):
    __tablename__ = 'impacts'
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicators.id'))
    entry_id = db.Column(db.Integer, db.ForeignKey('entries.id')) #db.relationship('Post', backref='author')
    coefficient = db.Column(db.String)
    
    def __repr__(self):
        return '<indicator_id %r>' % self.indicator_id

class Geography(db.Model):
    __tablename__ = 'geographies'
    id = db.Column(db.String(255),primary_key = True)
    short_name = db.Column(db.String(256))
    name = db.Column(db.String(256))
    
    def __repr__(self):
        return '<short_name %r>' % self.short_name
    
# Schema Objects
class IndicatorObject(SQLAlchemyObjectType):
    class Meta:
        model = Indicator
        interfaces = (graphene.relay.Node, )

class GeographyObject(SQLAlchemyObjectType):
    class Meta:
        model = Geography
        interfaces = (graphene.relay.Node, )
        
class EntryObject(SQLAlchemyObjectType):
    class Meta:
        model = Entry
        interfaces = (graphene.relay.Node, )
        
class ImpactObject(SQLAlchemyObjectType):
    class Meta:
        model = Impact
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    allIndicatores = SQLAlchemyConnectionField(IndicatorObject)
    allGeographies = SQLAlchemyConnectionField(GeographyObject)
    allEntries = SQLAlchemyConnectionField(EntryObject)
    allImpacts = SQLAlchemyConnectionField(ImpactObject)
    
    
schema = graphene.Schema(query=Query)

@app.route('/')
def home():
    return 'home'

# Routes
...
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')