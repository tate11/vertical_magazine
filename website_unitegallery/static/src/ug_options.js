function importScript(name) {
    var s = document.createElement("script");
    s.src = "unitegallery/themes/" + name;
    document.querySelector("head").appendChild(s);
}

(function() {
    'use strict';
    var website = odoo.website;
    website.odoo_website = {};
    
    website.snippet.options.ug_theme_carousel = website.snippet.Option.extend({
        importScrpt("carousel/ug-theme-carousel.js")
    })
    
})();