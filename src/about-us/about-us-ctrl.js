angular.module('CS6310').controller('AboutUsCtrl', function () {
    var ctrl = this;

    var developers = [
        {
            name: 'Aaron Buxbaum',
            text: 'I am a Web Developer at Google, on the Maps Local Guides program. I specialize in AngularJS and Javascript.',
            image: 'https://media.licdn.com/mpr/mpr/shrinknp_400_400/p/2/005/01c/0ac/0ece994.jpg',
            link: 'https://www.linkedin.com/in/aaronbuxbaum'
        }
    ];

    ctrl.developers = _.shuffle(developers);
});