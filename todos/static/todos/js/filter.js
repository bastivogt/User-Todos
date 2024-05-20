const filter_elements = {
    tags: document.querySelectorAll("[data-filter-key]")
};

function filter_get_params(elements) {
    const url = new URL(location.href);
    const params = new URLSearchParams(url.search);
    elements.forEach((tag) => {
        tag.addEventListener("click", (e) => {
            e.preventDefault();
            const key = e.target.dataset.filterKey;
            const value = e.target.dataset.filterValue
            params.set(key, value);
            location.href = `?${params.toString()}`;

        });
    });
}

document.addEventListener("DOMContentLoaded", (e) => {
    console.log("filter.js loaded");
    filter_get_params(filter_elements.tags);
});

