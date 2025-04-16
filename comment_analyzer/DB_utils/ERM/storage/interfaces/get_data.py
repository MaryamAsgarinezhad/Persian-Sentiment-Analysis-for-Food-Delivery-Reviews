from sqlalchemy.orm import sessionmaker
from ....ERM.config.db import engine
from sqlalchemy import text


Session = sessionmaker(bind=engine)


def get_comments(vendor_id):
    with Session() as session:
        query = text('SELECT comment_id, foods, comment_text FROM snap_restaurant_comments WHERE vendor_id=:vendor_id')
        result = session.execute(query, {'vendor_id': vendor_id})
        comments = []
        for row in result.fetchall():
            comment_dict = {
                'comment_id': row.comment_id,
                'foods': row.foods,
                'comment_text': row.comment_text
            }
            comments.append(comment_dict)

    return comments


def get_product(vendor_id, title):
    with Session() as session:
        query = text(
            'SELECT id, category_tile, product_title, description, vendor_id, title '
            'FROM snap_restaurant_products '
            'WHERE vendor_id=:vendor_id AND (title=:title OR title LIKE :partial_title)'
        )
        result = session.execute(query, {'vendor_id': str(vendor_id), 'title': title, 'partial_title': f'%{title}%'})
        product_obj = result.fetchone()
        if product_obj:
            return {
                'product_id': product_obj.id,
                'category_tile': product_obj.category_tile,
                'product_title': product_obj.product_title,
                'description': product_obj.description,
                'title': product_obj.title,
            }

        return None


def get_vendor(vendor_id):
    with Session() as session:
        query = text(
            'SELECT * '
            'FROM snap_restaurant_vendor '
            'WHERE id=:vendor_id'
        )
        result = session.execute(query, {'vendor_id': str(vendor_id)})
        vendor_obj = result.fetchone()
        if vendor_obj:
            return vendor_obj.vendor_code
        return None


def get_vendors():
    with Session() as session:
        query = text(
            "SELECT id, title FROM snap_restaurant_vendor WHERE establishment='CATERING' or establishment='RESTAURANT' or establishment='FASTFOOD'")
        result = session.execute(query)
        vendors = []
        for row in result.fetchall():
            vendors.append({"id": row.id, "title": row.title})
    return vendors


def get_comment_from_analyze(comment_id):
    with Session() as session:
        query = text('SELECT comment_id FROM analyzer_result WHERE comment_id=:comment_id')
        result = session.execute(query, {'comment_id': comment_id})
        comment_obj = result.fetchone()
        if comment_obj:
            return True
        return False
