const tabsBox = document.querySelector(".tabs-box"),
    allTabs = document.querySelectorAll(".tabs-box .tab"),
    arrlowIcons = document.querySelectorAll(".icon i");

let isDragging = false;

const handleIcons = () => {
    let scrollVal = Math.round(tabsBox.scrollLeft);
    let maxScrollableWidth = tabsBox.scrollWidth - tabsBox.clientWidth;

    // Right icon va left icon ko'rinishini boshqarish
    arrlowIcons[0].parentElement.style.display = scrollVal > 0 ? "flex" : "none";
    arrlowIcons[1].parentElement.style.display = maxScrollableWidth > scrollVal ? "flex" : "none";
}

arrlowIcons.forEach(icon => {
    icon.addEventListener("click", () => {
        // left yoki right icon bosilganda
        tabsBox.scrollLeft += icon.classList.contains("fa-angle-left") ? -350 : 350;
        setTimeout(() => handleIcons(), 50);
    });
});

// Tablarni bosganda ularni faollashtirish
allTabs.forEach(tab => {
    tab.addEventListener("click", () => {
        tabsBox.querySelector(".active")?.classList.remove("active"); // eski aktivni olib tashlash
        tab.classList.add("active"); // yangi aktivni qo'shish
    });
});

// Dragging uchun funksiyalar
const dragging = (e) => {
    if (!isDragging) return;
    tabsBox.classList.add("dragging");
    tabsBox.scrollLeft -= e.movementX;  // X harakatlanishini hisoblash
    handleIcons();
}

const dragStop = () => {
    isDragging = false;
    tabsBox.classList.remove("dragging");
}

// Mouse down (bosilgan paytda) va mouse move (harakatlangan paytda) event listenerlari
tabsBox.addEventListener("mousedown", () => isDragging = true);
tabsBox.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
