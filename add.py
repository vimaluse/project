class vimal:

    def prime(self,a):   
        if a >=2:
            for i in range(2,a):
                if a%i == 0:
                    print(a,"not prime")
                    break
            else:
                print(a, "prime")


    def palindrome(self,i):
        if str(i) == str(i)[::-1]:
            print(i,"palindrome")
        else:
            print(i,"not palindrome")


v1 = vimal()
v1.prime(11)
v1.palindrome(545)
