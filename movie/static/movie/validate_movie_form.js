const text_review = document.getElementById("id_text_review");
const rating = document.getElementById("id_rating");
const form = document.getElementById("review_form");
const review_form_errors = document.getElementById("review_form_errors");

form.addEventListener("submit", function(event){
    let form_valid = true;
    let error = "";
    if(text_review.value.length < 25){
        error += `<li>Переконайтеся, що рецензія містить не менше ніж 25 символів (зараз ${text_review.value.length})</li>`;
        form_valid = false;
    }

    if(text_review.value.length > 3000){
        error += `<li>Переконайтеся, що рецензія містить не більше ніж 3000 символів (зараз ${text_review.value.length})</li>`
        form_valid = false;
    }

    if(!rating.value){
        error += "<li>Дайте оцінку фільму</li>";
        form_valid = false;
    }
    
    if(!form_valid){
        review_form_errors.classList.remove("d-none");
        review_form_errors.innerHTML = "<ul>" + error + "</ul>";
        event.preventDefault();
    }
});