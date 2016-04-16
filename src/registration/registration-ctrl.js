angular.module('CS6310').controller('RegistrationCtrl', function($scope, $filter) {
  var ctrl = this;

  //EXAMPLE DATA
  ctrl.allClasses = [
    {
      subject: 'CS',
      number: 6476,
      title: 'Computer Vision'
    },
    {
      subject: 'CS',
      number: 6035,
      title: 'Introduction to Information Security'
    },
    {
      subject: 'CS',
      number: 6210,
      title: 'Advanced Operating Systems'
    },
    {
      subject: 'CS',
      number: 6250,
      title: 'Computer Networks',
      recommended: true
    },
    {
      subject: 'CSE',
      number: 6220,
      title: 'Intro to High-Performance Computing',
      recommended: true
    },
    {
      subject: 'CS',
      number: 6440,
      title: 'Intro to Health Informatics'
    },
    {
      subject: 'CS',
      number: 8803003,
      title: 'Special Topics: Reinforcement Learning'
    },
    {
      subject: 'CS',
      number: 6340,
      title: 'Software Analysis and Test'
    },
    {
      subject: 'CS',
      number: 6400,
      title: 'Database Systems Concepts and Design'
    },
    {
      subject: 'CS',
      number: 8803004,
      title: 'Special Topics: Embedded Software'
    },
    {
      subject: 'CSE',
      number: 8803005,
      title: 'Special Topics: Big Data for Health Informatics'
    },
    {
      subject: 'CS',
      number: 6601,
      title: 'Artificial Intelligence'
    }
  ];
  ctrl.selectedClasses = _.sampleSize(ctrl.allClasses, 2);
  ctrl.allClasses.map(function(item, i) {
    item.image = '//loremflickr.com/50/50?random=' + i;
    return item;
  });


  //Actual Functionality
  ctrl.querySearch = function(query) {
    return $filter('filter')(ctrl.allClasses, query);
  };
});