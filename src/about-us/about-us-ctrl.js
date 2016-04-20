angular.module('CS6310').controller('AboutUsCtrl', function () {
    var ctrl = this;

    var tempDevelopers = [
        {
            name: 'Aaron Buxbaum',
            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg',
            link: 'https://www.linkedin.com/in/aaronbuxbaum'
        },
        {
            name: 'Aaron Buxbaum',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        },
        {
            name: 'Aaron Buxbaum',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        },
        {
            name: 'Aaron Buxbaum',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        },
        {
            name: 'Aaron Buxbaum',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg',
            link: 'http://www.google.com'
        }
    ];

    ctrl.developers = _.shuffle(tempDevelopers);
});