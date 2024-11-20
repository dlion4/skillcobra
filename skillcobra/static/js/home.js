$(document).ready(function () {
    const category_items = [
        {
            icon: " uil-arrow",
            name: "Web Development",
        },
        {
            icon: "uil-graph-bar",
            name: "Bussiness",
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

    // Shuffle the category items array
    const shuffledItems = [...category_items].sort(() => 0.5 - Math.random());
    $("._cate101").each(function (index) {
        const iconClass = shuffledItems[index % shuffledItems.length].icon; // Cycle through icons if there are more elements
        $(this).find("i").addClass(iconClass + " cate_icon1"); // Add the icon class to the <i> element
    });
  
});
