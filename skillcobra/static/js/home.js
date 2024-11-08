$(document).ready(function () {
    const category_items = [
        {
            icon: " uil-arrow",
            name: "Web Development",
        },
        {
            icon: "uil-graph-bar",
            name: "Web Development",
        },
        {
            icon: "uil-monitor",
            name: "IT and Software",
        },
        {
            icon: "uil-ruler",
            name: "Design",
        },
        {
            icon: "uil-chart-line",
            name: "Marketing",
        },
        {
            icon: "uil-camera",
            name: "Photography",
        },
        {
            icon: "uil-music",
            name: "Music",
        },
    ];
    category_items.forEach(function (item) {
        const listItem = `<li><a href="#" class="ct_item"><i class='uil ${item.icon}'></i>${item.name}</a></li>`;
        $(".category_list").append(listItem);
    });
});
