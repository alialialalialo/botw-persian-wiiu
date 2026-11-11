#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define W 4096
int main(int c,char**v){
  FILE*f=fopen(v[1],"rb"); fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  uint8_t*s=malloc(n); if(fread(s,1,n,f)!=(size_t)n) return 1; fclose(f);
  uint8_t*o=malloc(n+n/8+64); long op=16;
  memcpy(o,"Yaz0",4); o[4]=n>>24;o[5]=n>>16;o[6]=n>>8;o[7]=n; memset(o+8,0,8);
  int HS=1<<16; int*head=malloc(HS*sizeof(int)); int*prev=malloc(n*sizeof(int)); for(int i=0;i<HS;i++)head[i]=-1;
  long i=0; long inserted=0;
  #define H(p) ((((p)[0]<<8)^((p)[1]<<4)^(p)[2])&(HS-1))
  while(i<n){
    long codepos=op++; o[codepos]=0;
    for(int b=0;b<8&&i<n;b++){
      int bl=0; long bd=0;
      if(i+2<n){
        while(inserted<i){ if(inserted+2<n){int h=H(s+inserted);prev[inserted]=head[h];head[h]=inserted;} inserted++; }
        int h=H(s+i); int p=head[h]; int tries=0;
        while(p>=0 && i-p<=W && tries<256){
          long m=0; long mx=n-i<273?n-i:273;
          while(m<mx && s[p+m]==s[i+m]) m++;
          if(m>bl){bl=m;bd=i-p; if(m==mx)break;}
          p=prev[p]; tries++;
        }
      }
      if(bl>=3){
        long d=bd-1;
        if(bl<18){ o[op++]=((bl-2)<<4)|(d>>8); o[op++]=d&255; }
        else { o[op++]=(d>>8); o[op++]=d&255; o[op++]=bl-18; }
        i+=bl;
      } else { o[codepos]|=0x80>>b; o[op++]=s[i++]; }
    }
  }
  f=fopen(v[2],"wb"); fwrite(o,1,op,f); fclose(f); return 0; }
