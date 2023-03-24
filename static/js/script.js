// Кнопка поиска

$(document).ready(function () {
  console.log("123");

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie("csrftoken");
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  $('[data-fancybox="gallery"]').fancybox({
    // Options will go here
  });

  $(".smoothScroll").on("click", function (e) {
    e.preventDefault();
    var target = this.hash,
      $target = $(target);

    $("html, body")
      .stop()
      .animate(
        {
          scrollTop: $target.offset().top,
        },
        900,
        "swing",
        function () {
          window.location.hash = target;
        }
      );
  });

  $(document).ready(function () {
    $(".animated-icon1,.animated-icon3,.animated-icon4").click(function () {
      $(this).toggleClass("open");
    });
  });
  // Обрез текста
  $(".box__news").each(function () {
    let size = 250;
    let newsText = $(this).text();
    if (newsText.length > size) {
      slicedText = newsText.slice(0, size);
      $(this).text(`${slicedText}...`);
    }
  });

  //owl-carousel initiazilation

  $("#owl-partners").owlCarousel({
    stagePadding: 50,
    loop: true,
    margin: 10,
    nav: true,
    responsive: {
      320: {
        items: 1,
      },
      600: {
        items: 3,
      },
      1000: {
        items: 5,
      },
    },
  });

  $("#owl-certs").owlCarousel({
    stagePadding: 50,
    loop: true,
    margin: 10,
    nav: true,
    responsive: {
      320: {
        items: 1,
      },
      600: {
        items: 3,
      },
      1000: {
        items: 5,
      },
    },
  });

  $("#owl-gallery").owlCarousel({
    loop: true,
    margin: 20,
    nav: true,
    responsive: {
      420: {
        items: 1,
      },
      600: {
        items: 2,
      },
      800: {
        items: 3,
      },
    },
  });

  // Просмотр+скачать
  $().fancybox({
    selector: ".owl-item:not(.cloned) a",
    hash: false,
    thumbs: {
      autoStart: true,
    },
    buttons: ["zoom", "download", "close"],
  });

  // // Плавная прокрутка

  // new SmoothScroll();

  // function SmoothScroll(el) {
  //   var t = this, h = document.documentElement;
  //   el = el || window;
  //   t.rAF = false;
  //   t.target = 0;
  //   t.scroll = 0;
  //   t.animate = function () {
  //     t.scroll += (t.target - t.scroll) * 0.1;
  //     if (Math.abs(t.scroll.toFixed(5) - t.target) <= 0.47131) {
  //       cancelAnimationFrame(t.rAF);
  //       t.rAF = false;
  //     }
  //     if (el == window) scrollTo(0, t.scroll);
  //     else el.scrollTop = t.scroll;
  //     if (t.rAF) t.rAF = requestAnimationFrame(t.animate);
  //   };
  //   el.onmousewheel = function (e) {
  //     e.preventDefault();
  //     e.stopPropagation();
  //     var scrollEnd = (el == window) ? h.scrollHeight - h.clientHeight : el.scrollHeight - el.clientHeight;
  //     t.target += (e.wheelDelta > 0) ? -70 : 70;
  //     if (t.target < 0) t.target = 0;
  //     if (t.target > scrollEnd) t.target = scrollEnd;
  //     if (!t.rAF) t.rAF = requestAnimationFrame(t.animate);
  //   };
  //   el.onscroll = function () {
  //     if (t.rAF) return;
  //     t.target = (el == window) ? pageYOffset || h.scrollTop : el.scrollTop;
  //     t.scroll = t.target;
  //   };
  // }

  // Счетчик
  $(".counter").counterUp({
    delay: 10,
    time: 1200,
    offset: 70,
    beginAt: 100,
    formatter: function (n) {
      return n.replace(/,/g, ".");
    },
  });
  $(".counter").addClass("animated fadeInDownBig");
  $("h2").addClass("animated fadeIn");

  // Выбрать несколько элементов

  $(".sort").click(function () {
    var mylist = $(".items");
    var listitems = mylist.children("li").get();
    listitems.sort(function (a, b) {
      var compA = $(a).data("selected");
      var compB = $(b).data("selected");
      return compA < compB ? 1 : compA > compB ? 1 : 0;
    });
    $.each(listitems, function (idx, itm) {
      mylist.append(itm);
    });
  });

  $("li", ".items").click(function () {
    var checks = $('[type="checkbox"]', ".checks");
    var item = $(this);

    if (item.data("selected") == "0") {
      item.data("selected", "1");
      item.addClass("selected");
    } else {
      item.data("selected", "0");
      item.removeClass("selected");
    }

    checks
      .filter('[data-guid="' + item.data("guid") + '"]')
      .prop("checked", item.data("selected") == "1");
  });

  $(document).on("change", ".file-input-field", function () {
    var $value = $(this).parent().next();
    $value.addClass("added").text(
      $(this)
        .val()
        .replace(/C:\\fakepath\\/i, "")
    );
  });
  $("#phone").mask("+7 (9999) 999 - 99 - 99", {
    completed: function () {
      alert("Да, этой мой номер");
    },
  });
  $("#phone2").mask("+7 (9999) 999 - 99 - 99", {
    completed: function () {
      alert("Да, этой мой номер");
    },
  });

  $("#order_service_button").click(function (event) {
    event.preventDefault();
    order = $("#order_form").serializeArray();
    $(".choose__item ul li").each(function () {
      if ($(this).hasClass("selected")) {
        // console.log('DATA', $(this).data('order'));
        order.push({ name: $(this).data("order"), value: "selected" });
      }
    });
    // console.table(order);
    console.log(order);
    $.post("/accept_order/", order)
      .done((response) => {
        if (response["order_id"]) {
          var id = response["order_id"];
          $(".modal-title:visible").text("Спасибо!");
          $(".modal__title__small__text:visible").hide();
          $(".modal-body:visible").html(`
            <h3 class="text text-info">
              Обращение зарегистрировано, идентификатор заявки ${id}
            </h3>
            <p class="text text-primary py-3">
              В ближайшее время с Вами свяжется наш специалист
            </p>
            `);
          $(".modal-footer:visible").hide();
        }

        if (response["errors"]) {
          $(".invalid-feedback").remove();
          $(".border").each(function () {
            $(this).removeClass("border border-danger");
          });
          for (let key in response["errors"]) {
            // remove all red borders
            // $('.border-danger').removeClass('is-invalid border border-danger');
            // $('.invalid-feedback:visible').hide();
            console.log(key, ":", response["errors"][key]);
            let form = $("#order_form");
            let element = form.find(`input[name="${key}"]`);

            // element.after(`<small class="text-danger">${response['errors'][key]}</small>`);
            element.addClass("is-invalid border border-danger");
            element.after(
              `<div class="invalid-feedback">${response["errors"][key]}</div>`
            );
            if (key == "captcha") {
              let captcha_div = $("#order_captcha_check");
              captcha_div.addClass("border border-danger");
              captcha_div.css("border-radius", "3px");
              $("#order_captcha_message").html(
                `<p class="text text-danger">
                  ${response["errors"][key]}
                </p>`
              );
            }
          }
        }
      })
      .fail((response) => {
        console.log("fail");
        console.log(response);
      });
  });
});
