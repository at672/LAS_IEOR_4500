#include<iostream>
#include<stdlib.h> 

using namespace std;

# define NN 2

double dot(int N, double* x, double* y)
//dot product of two vector:
//N: dimension; x,y: pointers of two arrays'starts
{
	double sum=0;
	for(int i=0;i<N;i++)
	{
		sum+=x[i]*y[i];
	}
	return sum;
}

double uni_rv()
//generate one uniform distributed random varible from [0,1]
{
	return float(rand())/RAND_MAX;
}


bool initial(int N, double* upbound,double* lowbound, double* x)
//First: examine the feasibility of upbound and lowbound of the QP problem
//Second: x is the starting protfolio protion that we want to find a feasible starting x. 
//        double* x is a pointer of array where we want to store the result of x.
//        initialize a feasible x by a random weighted method; The normalization of x can be ensured;
{
	bool mark=true;
	double sumlow=0,sumup=0,sumgap=0;
	double* gap=new double[N];
	for(int i=0;i<N;i++)
	{
		if(upbound[i]<lowbound[i]){cout<<"upbound < lowbound at "<<i<<endl;	return false;}
		sumlow+=lowbound[i];sumup+=upbound[i];	
		gap[i]=uni_rv()*(upbound[i]-lowbound[i]);
		sumgap+=gap[i];
	}
	
	if(sumlow>=1)
	{
	    if(sumlow==1)
	    {
			cout<<"portfolio vector should be the low bound"<<endl;
	        return false;
		}
		else
		{
			cout<<"Too big low bound"<<endl;
			return false;
		}
	}
	
	if(sumup<=1)
	{
	    if(sumup==1)
	    {
			cout<<"portfolio vector should be the up bound"<<endl;
	        return false;
		}
		else
		{
			cout<<"Too small up bound"<<endl;
			return false;
		}
	}
	cout<<"problem is feasible"<<endl;
	double weight=(1-sumlow)/sumgap;
	double collect=0;
	for(int i=0;i<N;i++)
	{
		x[i]=lowbound[i]+gap[i]*weight;
		collect+=x[i];
	}
	cout<<"normalization examination:"<<collect<<endl;
	return true;	
}

int GiveY(int N, double* g,double* y, double* x, double* cov, double* mu,double lambda, double* upbound,double* lowbound)
//The function is UNFINISHED!!
//The function is intended to give the y-vector (see professor's lecture <<algorithm II>>), that is the gradient descendent direction;
//N :dimension;   g: gradient of F-function; x: portfolio vector; cov: covariance matrix; mu: mean returns of assets;
//lambda: the lambda in F-function
//Finished part: g has been calculated
//Remaining part: sort g, find m, find y, restore the position of y, return it.
{
	int plus;
	for(int i=0;i<N;i++)
	{
		plus=dot(N,&cov[i*N],x);
		g[i]=2*lambda*plus-mu[i];
	}
	// double sort g;
	// compute m
	// return y buy output
	return 0;
}


double GiveS(int N,double* g, double* y, double* cov, double lambda) 
// After finding y, this function gives the s.
{
	double s=dot(N,g,y);
	double* temp= new double[N];
	for(int i=0;i<N;i++)
	{
		temp[i]=dot(N,&cov[i*N],y);
	}
	s=s/dot(N,temp,y);
	s=s/(-2*lambda);
	if(s>1) s=0.99;
	
	/* Below I cout the s because I am not sure whether the s will be negative. 
	theoretically speaking, it is impossible, since y is the decreasing direction. 
	But I am worried about the issue of accuracy will generate a s such as -0.00001*/
	cout<<"s is "<<s<<endl;
	/*
	if(s>1)
	{
		return 0.99;
	}
	else if(s<-0.01)
	{
		cout<<"find a s smaller than zero!"<<endl;
	}*/
	return s;
}

double GiveStep(int N, double* x,double* cov,double* mu, double lambda, double* lowbound,double* upbound)
//based on the above function GiveS and GiveY, the function performs gradient descendent for only one time
//First: get y and s;
//Second: move x; move_max record the maximun argument of x. move_max is the indicator of ending the loop (I think).
{
	double* y=new double[N];
	double* g=new double[N];
	GiveY(N,g,y,x,cov,mu,lambda,upbound,lowbound);
	double s;
	s=GiveS(N,g,y,cov,lambda);
	double move_max=0;
	double temp;
	for(int i=0;i<N;i++)
	{
		temp=s*y[i];
		x[i]+=temp;
		if(abs(temp)>move_max){move_max=abs(temp);}
	}
	return move_max;	
}

int main()
{
	/*	cov =[ 4 -1           mu = [ 2, 1 ]   lambda=1  	bound [0,1];
	          -1  1 ]	                                              	*/
	double *upbound=new double[NN];
	double *lowbound=new double[NN];
	double *cov=new double[NN*NN];
	double *mu= new double[NN];
	double *x = new double[NN];
	double lambda=1;
	upbound[0]=1;upbound[1]=1;lowbound[0]=0;lowbound[1]=0;
	cov[0]=4;cov[1]=-1;cov[2]=-1;cov[3]=1;
	mu[0]=2;mu[1]=1;

	bool feasible;
	feasible=initial(NN,upbound,lowbound,x);
	if(feasible==false)
	{
		cout<<"problem infeasible"<<endl;
		return 1;
	}
	double eps; // decide when the loop below will end. if max item of |Xn+1 - Xn| < epsilon, end it.
	//cin>>eps;
	double size;
	eps=0.01;
	while(true)
	{
		size=GiveStep(NN,x,cov,mu,lambda,lowbound,upbound);
		if(size<eps)break;
	}
	
	
	
	
	
	
	/* Test Code of GiveS
	cout<<NN<<endl;
	double* testg=new double[NN];
	testg[0]=1;testg[1]=2;
	double* testy=new double[NN];
	testy[0]=3;testy[1]=4;	
	cout<<GiveS(NN,testg,testy,cov,lambda)<<endl;
	*/	
	return 0;
}










