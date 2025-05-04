from src.models.category import Category


def test_full_category_service_workflow(category_service):
    """Full integration test for all service operation"""

    # 1. Test add_category
    lazer = Category(id=None, name="Lazer")
    lazer_id = category_service.add_category(lazer).id
    assert lazer_id is not None

    # 2. Test add_category
    alimentacao = Category(id=None, name="Alimentação")
    alimentacao_id = category_service.add_category(alimentacao).id
    assert alimentacao_id is not None

    # 3. Test get_all_categories
    categories = category_service.get_all_categories()
    assert len(categories) == 2
    assert any(c.name == lazer.name for c in categories)

    # 4. Test get_category_by_id
    alimentacao_category = category_service.get_category_by_id(alimentacao_id)
    assert alimentacao_category.name == "Alimentação"

    # 5. Test update_category
    lazer.name = "Lazer 2"
    assert category_service.update_category(lazer) is True
    assert category_service.get_category_by_id(lazer_id).name == "Lazer 2"

    # 6. Test delete_category
    assert category_service.delete_category(lazer_id) is True
    assert len(category_service.get_all_categories()) == 1
