package main
// it dont have exceptions
// it has only for loop
import (
	"fmt"
	"errors"
)

//struct in golang

type person struct {
	name string
	age int
	
}

func inc (x *int){
	*x++
}

//import "os" //excessive - we are not using any function in this package

func main() {
	//structures in go lang
	p1 := person{name : "Bhavesh", age : 23}
	fmt.Println(p1)
	fmt.Println(p1.name,p1.age)
	//.........................//
	//pointers in golang
	i_new := 7
	inc(&i_new)
	fmt.Println(i_new)
	//.........................//
	x:=55 
	Y:=-1
	//z := [5]int{5,6,7}
	z := []int{5,6,7}
	z = append(z, 13)
	//key value pair in golan
	//var_name =make(map[key_type]value_type)
	var_name := make(map[string]int)
	var_name["example"]=007
	
	if (Y>2) {
		fmt.Println("Hello world",x,Y)
	} else if (Y>-2){
		delete(var_name , "example")
		var_name["new_egg"]=0
		fmt.Println("Hello nothing",z,var_name)
	} else{
		fmt.Println("Hello....!",z)	
	}
	
	//LOOPS
	
	for i:=0; i<5; i++{
		fmt.Println("hi hello",i)
	}
	
	// while
	
	i:=0
	for i<5{
		fmt.Println("hi hello",i)
		i++
	}

	// for a loop range
	
	arr := []string{"a","b","c"}
	arr = append(arr,"hdjasdj")
	
	for index,value := range arr {
		ans,err := sum(index,-1)  // function with multipal return values
		if err == nil{
			fmt.Println(arr[index],index,value,ans)
		} else {
			fmt.Println(err)
		}
	}
	for key,value := range var_name {
		fmt.Println(var_name[key],key,value)
	}
	
}


func sum(x int, y int) (int,error) {
	if y<0{
		return 0,errors.New("example error for values less then zero")
	}
	return x+y,nil
}
