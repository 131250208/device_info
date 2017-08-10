/**
 * Created by wycheng on 8/10/17.
 */
var app_add_editor = angular.module('manager_app', []);
app_add_editor.controller('validateCtrl', function ($scope) {

});

app_add_editor.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});