from flask import Blueprint, request, jsonify, make_response
from . import db_session
from .news import News

blueprint = Blueprint("news_api", __name__)


@blueprint.route("/api/news", methods=["GET"])
def get_all_news():
    dbsess = db_session.create_session()
    news = [n.to_dict(only=["title", "content", "user.name"]) for n in dbsess.query(News).all()]
    return jsonify({"news": news})


@blueprint.route("/api/news/<int::news_id>", methods=["GET"])
def get_one_news(news_id):
    dbsess = db_session.create_session()
    news = dbsess.query(News).filter(News.id == news_id).first()
    if not news:
        return jsonify({"Error": "not_found"}, 404)
    return jsonify({"news": news.to_dict(only=["title", "content", "user.name"])})



@blueprint.route("/api/news", methods=["POST"])
def add_news():
    pass


@blueprint.route("api/news", methods=["DELETE"])
def delete_news():
    pass


@blueprint.route("api/news", methods=["PUT"])
def update_news():
    pass


