// Background color
image_1 = 'https://www.rentokil.com/blog/wp-content/uploads/2017/04/malaria-net-with-children.jpg';
image_2 = 'https://images.theconversation.com/files/165596/original/image-20170418-32705-lx8dyb.jpg?ixlib=rb-1.1.0&rect=299%2C149%2C4700%2C2282&q=45&auto=format&w=1356&h=668&fit=crop';
image_3 = 'https://cdn.the-scientist.com/assets/articleNo/65777/aImg/31650/malaria-vaccine-article-m.jpg';

var images = new Array(image_1,image_2,image_3);

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;

  var dots = document.getElementsByClassName("dot");
  if (n > images.length) {slideIndex = 1} 
  if (n < 1) {slideIndex = images.length}
  
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" dot-active", "");
  }

  $("#background")
        .attr("style", "background-image: url("+images[slideIndex-1]+");background-size: 100%; height: 100%;");

  dots[slideIndex-1].className += " dot-active";

}


