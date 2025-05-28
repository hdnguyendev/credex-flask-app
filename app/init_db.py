from app import create_app, db
from app.models import Category

def init_db():
    app = create_app()
    with app.app_context():
        # Tạo tất cả các bảng
        db.create_all()
        
        # Thêm các phân loại mặc định nếu chưa tồn tại
        default_categories = [
            'Công việc',
            'Học tập',
            'Mạng xã hội',
            'Email',
            'Tài chính',
            'Giải trí'
        ]
        
        for category_name in default_categories:
            if not Category.query.filter_by(name=category_name).first():
                category = Category(name=category_name)
                db.session.add(category)
        
        db.session.commit()
        print("Database đã được khởi tạo thành công!")

if __name__ == '__main__':
    init_db() 