from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, BooleanField, FileField,
    FloatField, SelectField, SubmitField, IntegerField, DateTimeField,
    TimeField, DateField, SelectMultipleField
)
from wtforms.validators import DataRequired, Email, Optional, Length

class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Увійти')

class BlockForm(FlaskForm):
    title = StringField('Заголовок (UA)', validators=[DataRequired(), Length(max=120)])
    title_en = StringField('Заголовок (EN)', validators=[Optional(), Length(max=120)])
    title_de = StringField('Заголовок (DE)', validators=[Optional(), Length(max=120)])
    title_ru = StringField('Заголовок (RU)', validators=[Optional(), Length(max=120)])
    
    content = TextAreaField('Текст (UA)', validators=[Optional(), Length(max=4000)])
    content_en = TextAreaField('Текст (EN)', validators=[Optional(), Length(max=4000)])
    content_de = TextAreaField('Текст (DE)', validators=[Optional(), Length(max=4000)])
    content_ru = TextAreaField('Текст (RU)', validators=[Optional(), Length(max=4000)])
    
    image = FileField('Зображення', validators=[Optional()])
    is_active = BooleanField('Активний')
    is_top = BooleanField('Головний блок')
    submit = SubmitField('Зберегти')

class PaymentMethodForm(FlaskForm):
    name = StringField('Назва (UA)', validators=[DataRequired(), Length(max=120)])
    name_en = StringField('Назва (EN)', validators=[Optional(), Length(max=120)])
    name_de = StringField('Назва (DE)', validators=[Optional(), Length(max=120)])
    name_ru = StringField('Назва (RU)', validators=[Optional(), Length(max=120)])
    type = SelectField('Тип', choices=[
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank', 'Банк/QR'),
        ('btc', 'Bitcoin (BTC)'),
        ('eth', 'Ethereum (ETH)'),
        ('usdc', 'USD Coin (USDC)'),
        ('custom', 'Інший')
    ])
    details = TextAreaField('Реквізити (JSON)', validators=[Optional(), Length(max=2000)])
    qr_code = FileField('QR-код', validators=[Optional()])
    description_ua = TextAreaField('Опис (UA)', validators=[Optional(), Length(max=2000)])
    description_en = TextAreaField('Опис (EN)', validators=[Optional(), Length(max=2000)])
    description_de = TextAreaField('Опис (DE)', validators=[Optional(), Length(max=2000)])
    description_ru = TextAreaField('Опис (RU)', validators=[Optional(), Length(max=2000)])
    is_active = BooleanField('Активний')
    submit = SubmitField('Зберегти')

class SettingsForm(FlaskForm):
    facebook = StringField('Facebook', validators=[Optional(), Length(max=120)])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=120)])
    telegram = StringField('Telegram', validators=[Optional(), Length(max=120)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField('Зберегти')

class DaoProposalForm(FlaskForm):
    title = StringField('Заголовок предложения', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Описание предложения', validators=[DataRequired(), Length(max=2000)])
    duration_days = IntegerField('Продолжительность голосования (дни)', validators=[DataRequired()], default=14)
    min_tokens_to_vote = FloatField('Минимум токенов для голосования', validators=[DataRequired()], default=1.0)
    submit = SubmitField('Создать предложение')

class ProductForm(FlaskForm):
    """Форма для создания/редактирования продукта"""
    name = StringField('Название (UA)', validators=[DataRequired(), Length(max=128)])
    name_en = StringField('Название (EN)', validators=[Optional(), Length(max=128)])
    name_de = StringField('Название (DE)', validators=[Optional(), Length(max=128)])
    name_ru = StringField('Название (RU)', validators=[Optional(), Length(max=128)])
    
    slug = StringField('URL (slug)', validators=[DataRequired(), Length(max=128)])
    
    description = TextAreaField('Описание (UA)', validators=[DataRequired(), Length(max=4000)])
    description_en = TextAreaField('Описание (EN)', validators=[Optional(), Length(max=4000)])
    description_de = TextAreaField('Описание (DE)', validators=[Optional(), Length(max=4000)])
    description_ru = TextAreaField('Описание (RU)', validators=[Optional(), Length(max=4000)])
    
    category_id = SelectField('Категория', coerce=int, validators=[DataRequired()])
    
    price = FloatField('Цена (EUR)', validators=[DataRequired()])
    token_price = FloatField('Цена в токенах', validators=[Optional()])
    
    example_url = StringField('Ссылка на пример', validators=[Optional(), Length(max=512)])
    delivery_time = StringField('Время выполнения', validators=[Optional(), Length(max=128)])
    support_period = StringField('Период поддержки', validators=[Optional(), Length(max=128)])
    
    features = TextAreaField('Функции (по одной на строку)', validators=[Optional(), Length(max=2000)])
    
    image = FileField('Главное изображение', validators=[Optional()])
    is_digital = BooleanField('Цифровой продукт')
    is_active = BooleanField('Активен')
    
    submit = SubmitField('Сохранить')

class ProductImageForm(FlaskForm):
    """Форма для добавления изображений к продукту"""
    image = FileField('Изображение', validators=[DataRequired()])
    title = StringField('Заголовок', validators=[Optional(), Length(max=128)])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    is_main = BooleanField('Главное изображение')
    submit = SubmitField('Добавить изображение')

class CategoryForm(FlaskForm):
    """Форма для создания/редактирования категории"""
    name = StringField('Название (UA)', validators=[DataRequired(), Length(max=64)])
    name_en = StringField('Название (EN)', validators=[Optional(), Length(max=64)])
    name_de = StringField('Название (DE)', validators=[Optional(), Length(max=64)])
    name_ru = StringField('Название (RU)', validators=[Optional(), Length(max=64)])
    
    slug = StringField('URL (slug)', validators=[DataRequired(), Length(max=64)])
    
    description = TextAreaField('Описание (UA)', validators=[Optional(), Length(max=2000)])
    description_en = TextAreaField('Описание (EN)', validators=[Optional(), Length(max=2000)])
    description_de = TextAreaField('Описание (DE)', validators=[Optional(), Length(max=2000)])
    description_ru = TextAreaField('Описание (RU)', validators=[Optional(), Length(max=2000)])
    
    image = FileField('Изображение', validators=[Optional()])
    is_active = BooleanField('Активна')
    order = IntegerField('Порядок', validators=[Optional()], default=1)
    
    submit = SubmitField('Сохранить')

# Blog Forms
class BlogBlockForm(FlaskForm):
    """Form for editing blog blocks"""
    title = StringField('Заголовок (UA)', validators=[DataRequired(), Length(max=255)])
    title_en = StringField('Заголовок (EN)', validators=[Optional(), Length(max=255)])
    title_de = StringField('Заголовок (DE)', validators=[Optional(), Length(max=255)])
    title_ru = StringField('Заголовок (RU)', validators=[Optional(), Length(max=255)])
    
    content = TextAreaField('Контент (UA)', validators=[DataRequired()])
    content_en = TextAreaField('Контент (EN)', validators=[Optional()])
    content_de = TextAreaField('Контент (DE)', validators=[Optional()])
    content_ru = TextAreaField('Контент (RU)', validators=[Optional()])
    
    summary = TextAreaField('Краткое описание (UA)', validators=[Optional(), Length(max=500)])
    summary_en = TextAreaField('Краткое описание (EN)', validators=[Optional(), Length(max=500)])
    summary_de = TextAreaField('Краткое описание (DE)', validators=[Optional(), Length(max=500)])
    summary_ru = TextAreaField('Краткое описание (RU)', validators=[Optional(), Length(max=500)])
    
    featured_image = FileField('Изображение', validators=[Optional()])
    is_active = BooleanField('Активен', default=True)
    
    submit = SubmitField('Сохранить')

class BlogTopicForm(FlaskForm):
    """Form for creating and managing blog topics"""
    title = StringField('Название темы', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=1000)])
    priority = IntegerField('Приоритет', validators=[Optional()], default=0)
    status = SelectField('Статус', choices=[
        ('pending', 'Ожидает'),
        ('scheduled', 'Запланировано'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено')
    ], default='pending')
    
    submit = SubmitField('Сохранить')

class TopicBulkImportForm(FlaskForm):
    """Form for bulk importing blog topics"""
    topics_text = TextAreaField('Темы (по одной на строку)', validators=[DataRequired()])
    submit = SubmitField('Импортировать')
    
class PublicationScheduleForm(FlaskForm):
    """Form for scheduling automatic blog posts"""
    topic_id = SelectField('Тема', coerce=int, validators=[Optional()])
    platform = SelectField('Платформа', choices=[
        ('blog', 'Блог'),
        ('telegram', 'Telegram'),
        ('all', 'Все платформы')
    ], default='all')
    
    repeat_weekly = BooleanField('Повторять еженедельно', default=False)
    day_of_week = SelectField('День недели', choices=[
        ('0', 'Понедельник'),
        ('1', 'Вторник'),
        ('2', 'Среда'),
        ('3', 'Четверг'),
        ('4', 'Пятница'),
        ('5', 'Суббота'),
        ('6', 'Воскресенье')
    ], validators=[Optional()])
    
    time_of_day = StringField('Время (ЧЧ:ММ)', validators=[Optional()])
    scheduled_time = DateTimeField('Дата и время публикации', format='%Y-%m-%d %H:%M', validators=[Optional()])
    
    submit = SubmitField('Запланировать')
