/*!
 * Star Rating <LANG> Translations
 *
 * This file must be loaded after 'star-rating.js'. Patterns in braces '{}', or
 * any HTML markup tags in the messages must not be converted or translated.
 *
 * NOTE: this file must be saved in UTF-8 encoding.
 *
 * @see http://github.com/kartik-v/bootstrap-star-rating
 * @author Kartik Visweswaran <kartikv2@gmail.com>
 */
(function ($) {
    "use strict";
    $.fn.ratingLocales['<LANG>'] = {
        defaultCaption: '{rating} звезди',
        starCaptions: {
            0.5: 'Половин звезда',
            1: 'Една звезда',
            1.5: 'Звезда и половина',
            2: 'Две звезди',
            2.5: 'Две звезди и',
            3: 'Три звезди',
            3.5: 'Три звезди и половина',
            4: 'Четири звезди',
            4.5: 'Четири звезди и половина',
            5: 'Пет звезди'
        },
        clearButtonTitle: 'Изчисти',
        clearCaption: 'Не е оценен'
    };
})(window.jQuery);
