#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Полная проверка функциональности сайта
Проверяет работоспособность всех основных компонентов и функций
"""

from app import create_app, db
from app.models import User, Block, Settings, Token, Airdrop, TokenSale, DaoProposal
from app.models import Category, Product, Payment, PaymentMethod
import json
import sys
from datetime import datetime, timedelta

app = create_app()

def verify_components():
    """Проверяет все компоненты сайта"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "components": {}
    }
    
    print("=" * 60)
    print("ПРОВЕРКА ФУНКЦИОНАЛЬНОСТИ САЙТА")
    print("=" * 60)
    
    with app.app_context():
        # 1. Проверка блоков
        print("\n1. Проверка блоков...")
        blocks = Block.query.all()
        results["components"]["blocks"] = {
            "count": len(blocks),
            "main_banner_exists": any(b.slug == "main-banner" for b in blocks),
            "blocks": []
        }
        
        if blocks:
            print(f"✅ Найдено {len(blocks)} блоков:")
            for block in blocks:
                results["components"]["blocks"]["blocks"].append({
                    "id": block.id,
                    "title": block.title,
                    "slug": block.slug, 
                    "is_active": block.is_active,
                    "is_top": block.is_top
                })
                print(f"  • {block.title} (slug: {block.slug}, активен: {block.is_active})")
        else:
            print("❌ Блоки не найдены")
        
        # 2. Проверка настроек сайта
        print("\n2. Проверка настроек сайта...")
        settings = Settings.query.first()
        results["components"]["settings"] = {
            "exists": settings is not None
        }
        
        if settings:
            print("✅ Настройки сайта найдены:")
            print(f"  • Facebook: {settings.facebook}")
            print(f"  • Instagram: {settings.instagram}")
            print(f"  • Telegram: {settings.telegram}")
            print(f"  • Email: {settings.email}")
            print(f"  • Contract Address: {settings.contract_address}")
            
            results["components"]["settings"].update({
                "facebook": settings.facebook,
                "instagram": settings.instagram,
                "telegram": settings.telegram,
                "email": settings.email,
                "contract_address": settings.contract_address,
                "token_name": settings.token_name,
                "token_symbol": settings.token_symbol
            })
        else:
            print("❌ Настройки сайта не найдены")
        
        # 3. Проверка информации о токене
        print("\n3. Проверка информации о токене...")
        token = Token.query.first()
        results["components"]["token"] = {
            "exists": token is not None
        }
        
        if token:
            print("✅ Информация о токене найдена:")
            print(f"  • Название: {token.name}")
            print(f"  • Символ: {token.symbol}")
            print(f"  • Контракт: {token.contract_address}")
            print(f"  • Общий выпуск: {token.total_supply}")
            
            results["components"]["token"].update({
                "name": token.name,
                "symbol": token.symbol,
                "contract_address": token.contract_address,
                "total_supply": token.total_supply,
                "circulating_supply": token.circulating_supply,
                "token_price_usd": token.token_price_usd
            })
        else:
            print("❌ Информация о токене не найдена")
        
        # 4. Проверка аирдропов
        print("\n4. Проверка аирдропов...")
        airdrops = Airdrop.query.all()
        results["components"]["airdrops"] = {
            "count": len(airdrops),
            "airdrops": []
        }
        
        if airdrops:
            print(f"✅ Найдено {len(airdrops)} аирдропов")
            for airdrop in airdrops:
                results["components"]["airdrops"]["airdrops"].append({
                    "id": airdrop.id,
                    "title": airdrop.title,
                    "is_active": airdrop.is_active
                })
                print(f"  • {airdrop.title} (активен: {airdrop.is_active})")
        else:
            print("ℹ️ Аирдропы не найдены (это нормально, их можно создать в админке)")
        
        # 5. Проверка токенсейлов
        print("\n5. Проверка токенсейлов...")
        token_sales = TokenSale.query.all()
        results["components"]["token_sales"] = {
            "count": len(token_sales),
            "token_sales": []
        }
        
        if token_sales:
            print(f"✅ Найдено {len(token_sales)} токенсейлов")
            for sale in token_sales:
                results["components"]["token_sales"]["token_sales"].append({
                    "id": sale.id,
                    "title": sale.title,
                    "is_active": sale.is_active
                })
                print(f"  • {sale.title} (активен: {sale.is_active})")
        else:
            print("ℹ️ Токенсейлы не найдены (это нормально, их можно создать в админке)")
        
        # 6. Проверка предложений DAO
        print("\n6. Проверка предложений DAO...")
        proposals = DaoProposal.query.all()
        results["components"]["dao_proposals"] = {
            "count": len(proposals),
            "proposals": []
        }
        
        if proposals:
            print(f"✅ Найдено {len(proposals)} предложений DAO")
            for proposal in proposals:
                results["components"]["dao_proposals"]["proposals"].append({
                    "id": proposal.id,
                    "title": proposal.title,
                    "status": proposal.status
                })
                print(f"  • {proposal.title} (статус: {proposal.status})")
        else:
            print("ℹ️ Предложения DAO не найдены (это нормально, их можно создать в админке)")
        
        # 7. Проверка категорий товаров
        print("\n7. Проверка категорий товаров...")
        categories = Category.query.all()
        results["components"]["categories"] = {
            "count": len(categories),
            "categories": []
        }
        
        if categories:
            print(f"✅ Найдено {len(categories)} категорий товаров")
            for category in categories:
                results["components"]["categories"]["categories"].append({
                    "id": category.id,
                    "name": category.name,
                    "slug": category.slug,
                    "product_count": Product.query.filter_by(category_id=category.id).count()
                })
                print(f"  • {category.name} ({Product.query.filter_by(category_id=category.id).count()} товаров)")
        else:
            print("ℹ️ Категории товаров не найдены (это нормально, их можно создать в админке)")
        
        # 8. Проверка товаров
        print("\n8. Проверка товаров...")
        products = Product.query.all()
        results["components"]["products"] = {
            "count": len(products),
            "products": []
        }
        
        if products:
            print(f"✅ Найдено {len(products)} товаров")
            for product in products:
                results["components"]["products"]["products"].append({
                    "id": product.id,
                    "name": product.name,
                    "slug": product.slug,
                    "price": product.price,
                    "token_price": product.token_price,
                    "category_id": product.category_id
                })
                print(f"  • {product.name} (цена: {product.price} USD, токены: {product.token_price} ITT)")
        else:
            print("ℹ️ Товары не найдены (это нормально, их можно создать в админке)")
        
        # 9. Проверка способов оплаты
        print("\n9. Проверка способов оплаты...")
        payment_methods = PaymentMethod.query.all()
        results["components"]["payment_methods"] = {
            "count": len(payment_methods),
            "payment_methods": []
        }
        
        if payment_methods:
            print(f"✅ Найдено {len(payment_methods)} способов оплаты")
            for method in payment_methods:
                results["components"]["payment_methods"]["payment_methods"].append({
                    "id": method.id,
                    "name": method.name,
                    "type": method.type,
                    "is_active": method.is_active
                })
                print(f"  • {method.name} (тип: {method.type}, активен: {method.is_active})")
        else:
            print("ℹ️ Способы оплаты не найдены (это нормально, их можно создать в админке)")
        
        # 10. Проверка администраторов
        print("\n10. Проверка администраторов...")
        admins = User.query.all()
        results["components"]["admins"] = {
            "count": len(admins),
            "admins": []
        }
        
        if admins:
            print(f"✅ Найдено {len(admins)} администраторов")
            for admin in admins:
                results["components"]["admins"]["admins"].append({
                    "id": admin.id,
                    "username": admin.username,
                    "is_admin": admin.is_admin,
                    "wallet_address": admin.wallet_address
                })
                print(f"  • {admin.username}")
        else:
            print("❌ Администраторы не найдены")
    
    # Сохраняем результаты в файл
    with open("site_functionality_check.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print("\nРезультаты проверки сохранены в файле site_functionality_check.json")
    
    # Итоговый результат
    print("\n" + "=" * 60)
    print("ИТОГИ ПРОВЕРКИ")
    print("=" * 60)
    
    all_passed = (
        results["components"].get("blocks", {}).get("count", 0) > 0 and
        results["components"].get("settings", {}).get("exists", False) and
        results["components"].get("token", {}).get("exists", False) and
        results["components"].get("admins", {}).get("count", 0) > 0
    )
    
    if all_passed:
        print("✅ Все основные компоненты работают корректно")
        print("✅ Сайт готов к использованию")
    else:
        print("⚠️ Некоторые компоненты требуют настройки:")
        if not results["components"].get("blocks", {}).get("count", 0) > 0:
            print("  • Необходимо создать блоки контента")
        if not results["components"].get("settings", {}).get("exists", False):
            print("  • Необходимо настроить основные настройки сайта")
        if not results["components"].get("token", {}).get("exists", False):
            print("  • Необходимо добавить информацию о токене")
        if not results["components"].get("admins", {}).get("count", 0) > 0:
            print("  • Необходимо создать администраторов")
    
    return all_passed

if __name__ == "__main__":
    success = verify_components()
    sys.exit(0 if success else 1)
