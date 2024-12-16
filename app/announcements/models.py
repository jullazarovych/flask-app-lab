from app import db

announcement_topics = db.Table(
    'announcement_topics',
    db.Column('announcement_id', db.Integer, db.ForeignKey('announcements.id'), primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('topics.id'), primary_key=True)
)

class Announcement(db.Model):
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  

    user = db.relationship('User', backref='announcements')  
    topics = db.relationship('Topic', secondary=announcement_topics, back_populates='announcements')  

    def __repr__(self):
        return f"<Announcement {self.name}>"

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    announcements = db.relationship('Announcement', secondary=announcement_topics, back_populates='topics')

    def __repr__(self):
        return f"<Topic {self.name}>"
