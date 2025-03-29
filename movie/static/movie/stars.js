const id_rating = document.getElementById("id_rating");
const stars = document.querySelectorAll('.star');

 for (let i = 0; i < stars.length; i++) {
    // if mouse is over star, it and all previous stars will change color
     stars[i].addEventListener("mouseover", function(){
        for(let j = 0; j < stars.length; j++){
            if(j <= i){
                stars[j].style.fill = "#FFD700";
            }
            else{
                stars[j].style.fill = "white";
            }
        }
     });
     
     // set the rating value when a star is clicked
     stars[i].addEventListener("click", function(){
        id_rating.value = i + 1;
     });

     // restore the selected rating when the mouse leaves the stars 
     stars[i].addEventListener("mouseout", function(){
        let rating = 0;
        if(id_rating.value){
            rating = id_rating.value;
        }

        for(let j = 0; j < rating; j++){
            stars[j].style.fill = "#FFD700";
        }
        
        for(let j = rating; j < stars.length; j++){
            stars[j].style.fill = "white";
        }
     });

 }
