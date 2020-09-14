#include <smmintrin.h>       //SSE
#include <iostream>
#include <ctime>
 
 
float inner_product(const float* x, const float* y, const long & len){
    float prod = 0.0f;
    long i;
    for (i=0;i<len;i++){
        prod+=x[i]*y[i];
    }
    return prod;
}
 
float dot_product(const float* x, const float* y, const long & len){
    float prod = 0.0f;
    const int mask = 0xff;        
    __m128 X, Y;
    float tmp;
    long i;
    for (i=0;i<len;i+=4){
        //_mm_loadu_ps把float转为__m128
        X=_mm_loadu_ps(x+i); 
        Y=_mm_loadu_ps(y+i);
        //_mm_storeu_ps把__m128转为float。_mm_dp_ps计算向量内积
        _mm_storeu_ps(&tmp,_mm_dp_ps(X,Y,mask));
    }
    return prod;
}
 
int main(){
    const int len1 = 10;
    float arr[len1]={2.0f,5.0f,3.0f,1.0f,7.0f,9.0f,4.0f,3.0f,7.0f,5.0f};
    float brr[len1]={9.0f,0.0f,3.0f,5.0f,3.0f,7.0f,8.0f,2.0f,6.0f,1.0f};
    std::cout<<"蛮力计算内积 "<<inner_product(arr,brr,len1)<<std::endl;
    std::cout<<"使用SSE计算内积 "<<dot_product(arr,brr,len1)<<std::endl;
 
    const int len2 = 1000000;
    float *crr=new float[len2];
    float *drr=new float[len2];
    for (int i=0;i<len2;i++){
        int value=i%10;
        crr[i]=value;
        drr[i]=value;
    }
 
    float prod;
    clock_t begin;
    clock_t end;
    begin=clock();
    prod=inner_product(crr,drr,len2);
    end=clock();
    std::cout<<"蛮力计算内积 "<<prod<<"\t用时"<<(double)(end-begin)/CLOCKS_PER_SEC<<"秒"<<std::endl;
    begin=clock();
    prod=dot_product(crr,drr,len2);
    end=clock();
    std::cout<<"使用SSE计算内积 "<<prod<<"\t用时"<<(double)(end-begin)/CLOCKS_PER_SEC<<"秒"<<std::endl;
}
 
//g++ -m32 -msse4.1 dp.cpp -o dp