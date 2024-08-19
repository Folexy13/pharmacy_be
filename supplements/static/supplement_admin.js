document.addEventListener("DOMContentLoaded", function () {
	let categoryField = document.getElementById("id_categories");
	let mainCategoryField = document.getElementById("id_main_category");
	let subcategoryField = document.getElementById("id_subcategories");

	function updateCategoryOptions() {
		const mainCategoryId = mainCategoryField.value;
		const selectedCategoryIds = Array.from(categoryField.selectedOptions).map(
			(option) => option.value
		);

		// Clear current options
		categoryField.innerHTML = '<option value="">Select category</option>';

		if (!mainCategoryId) {
			return;
		}

		const xhr = new XMLHttpRequest();
		xhr.open(
			"GET",
			"/supplements/categorylist/?main_category=" + mainCategoryId,
			true
		);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 400) {
				const { categories } = JSON.parse(xhr.responseText);
				for (const category of categories) {
					const option = document.createElement("option");
					option.value = category.id;
					option.textContent = category.name;

					// Retain selected categories
					if (selectedCategoryIds.includes(String(category.id))) {
						option.selected = true;
					}

					categoryField.appendChild(option);
				}
			} else {
				console.error("Failed to fetch categories:", xhr.statusText);
			}
		};

		xhr.onerror = function () {
			console.error("Request error...");
		};

		xhr.send();
	}

	function updateSubcategoryOptions() {
		const categoryIds = Array.from(categoryField.selectedOptions).map(
			(option) => option.value
		);
		const selectedSubcategoryIds = Array.from(
			subcategoryField.selectedOptions
		).map((option) => option.value);

		// Clear current options
		subcategoryField.innerHTML = '<option value="">Select subcategory</option>';

		if (categoryIds.length === 0) {
			return;
		}

		const xhr = new XMLHttpRequest();
		xhr.open(
			"GET",
			`/supplements/subcategorylist/?categories=${categoryIds.join(",")}`,
			true
		);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 400) {
				const { subcategories } = JSON.parse(xhr.responseText);

				for (const subcategory of subcategories) {
					const option = document.createElement("option");
					option.value = subcategory.id;
					option.textContent = subcategory.name;

					// Retain selected subcategories
					if (selectedSubcategoryIds.includes(String(subcategory.id))) {
						option.selected = true;
					}

					subcategoryField.appendChild(option);
				}
			} else {
				console.error("Failed to fetch subcategories:", xhr.statusText);
			}
		};

		xhr.onerror = function () {
			console.error("Request error...");
		};

		xhr.send();
	}

	mainCategoryField.addEventListener("change", updateCategoryOptions);
	categoryField.addEventListener("change", updateSubcategoryOptions);

	// Trigger changes on page load if needed
	if (mainCategoryField.value) {
		updateCategoryOptions();
	}
	if (categoryField.value) {
		updateSubcategoryOptions();
	}
});
