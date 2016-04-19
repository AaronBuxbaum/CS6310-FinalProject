angular.module('CS6310').controller('AboutUsCtrl', function () {
    var ctrl = this;

    var tempDevelopers = [
        {
            name: 'Aaron Buxbaum',
            title: 'Cool Dude',
            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg',
            actions: [
                {
                    link: 'AAAA',
                    name: 'Link 1'
                },
                {
                    link: 'BBBBB',
                    name: 'Link 2'
                }
            ]
        },
        {
            name: 'Aaron Buxbaum',
            title: 'Cool Dude',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        },
        {
            name: 'Aaron Buxbaum',
            title: 'Cool Dude',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        },
        {
            name: 'Aaron Buxbaum',
            title: 'Cool Dude',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        },
        {
            name: 'Aaron Buxbaum',
            title: 'Cool Dude',
            text: 'AAA',
            image: 'http://mediad.publicbroadcasting.net/p/kwmu/files/201508/tacos.jpg'
        }
    ];

    ctrl.developers = _.shuffle(tempDevelopers);
});