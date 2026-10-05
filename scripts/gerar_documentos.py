#!/usr/bin/env python3
"""Regenera diagramas e PDFs da Fase 1. Requer requirements-docs.txt.
As posições dos diagramas ficam neste arquivo; fontes textuais em docs/.
"""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from html import escape
import json, re, math, io, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, PageBreak
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1]
GREEN='#174C3C'; INK='#20312B'; MUTED='#52615A'; PALE='#E8F1E9'; GOLD='#F2C66D'
class Diagram:
 def __init__(self,title,w=1400,h=1000):self.title=title;self.w=w;self.h=h;self.nodes=[];self.edges=[]
 def box(self,id,x,y,w,h,title,body='',kind='box'):
  self.nodes.append(dict(id=id,x=x,y=y,w=w,h=h,title=title,body=body,kind=kind));return id
 def edge(self,a,b,points,label='',start='',end='',dash=False,arrow=False):
  self.edges.append(dict(a=a,b=b,points=points,label=label,start=start,end=end,dash=dash,arrow=arrow))
 def save(self,path):
  base=ROOT/path;base.parent.mkdir(parents=True,exist_ok=True)
  svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">',f'<title>{escape(self.title)}</title>','<rect width="100%" height="100%" fill="#ffffff"/>',f'<text x="35" y="38" font-family="Arial,sans-serif" font-size="26" font-weight="bold" fill="{GREEN}">{escape(self.title)}</text>']
  mx=Element('mxfile',host='app.diagrams.net',version='24.7.17');dg=SubElement(mx,'diagram',id='agenda',name=self.title);model=SubElement(dg,'mxGraphModel',dx=str(self.w),dy=str(self.h),page='1',pageWidth=str(self.w),pageHeight=str(self.h));root=SubElement(model,'root');SubElement(root,'mxCell',id='0');SubElement(root,'mxCell',id='1',parent='0')
  def txt(x,y,t,size=18,bold=False,anchor='start'):
   svg.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" text-anchor="{anchor}" fill="{INK}">{escape(t)}</text>')
  for i,e in enumerate(self.edges):
   pts=e['points'];svg.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{MUTED}" stroke-width="2"'+(' stroke-dasharray="8 5"' if e['dash'] else '')+'/>')
   if e['arrow']:
    x,y=pts[-1];px,py=pts[-2];ang=math.atan2(y-py,x-px)
    p1=(x-12*math.cos(ang-.45),y-12*math.sin(ang-.45));p2=(x-12*math.cos(ang+.45),y-12*math.sin(ang+.45))
    svg.append(f'<polyline points="{p1[0]},{p1[1]} {x},{y} {p2[0]},{p2[1]}" fill="none" stroke="{MUTED}" stroke-width="2"/>')
   if e['label']:
    a,b=pts[len(pts)//2-1],pts[len(pts)//2];txt((a[0]+b[0])/2,(a[1]+b[1])/2+22,e['label'],15,anchor='middle')
   for text,p,nextp in [(e['start'],pts[0],pts[1]),(e['end'],pts[-1],pts[-2])]:
    if text:
     dx=nextp[0]-p[0];dy=nextp[1]-p[1];norm=max(1,math.hypot(dx,dy));txt(p[0]+dx/norm*40,p[1]+dy/norm*40-12,text,17,True,'middle')
   cell=SubElement(root,'mxCell',id=f'e{i}',value=e['label'],style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;endArrow='+('open' if e['arrow'] else 'none')+';dashed='+str(int(e['dash']))+';fontSize=16;',edge='1',parent='1',source=e['a'],target=e['b']);geo=SubElement(cell,'mxGeometry',relative='1',**{'as':'geometry'});arr=SubElement(geo,'Array',**{'as':'points'})
   for x,y in pts[1:-1]:SubElement(arr,'mxPoint',x=str(x),y=str(y))
   for j,(s,pos) in enumerate([(e['start'],-.8),(e['end'],.8)]):
    if s:
     lab=SubElement(root,'mxCell',id=f'e{i}l{j}',value=s,style='edgeLabel;html=0;align=center;fontSize=17;resizable=0;',vertex='1',connectable='0',parent=f'e{i}');SubElement(lab,'mxGeometry',x=str(pos),y='-1',relative='1',**{'as':'geometry'})
  for n in self.nodes:
   x,y,w,h=n['x'],n['y'],n['w'],n['h'];kind=n['kind'];title=n['title'];lines=n['body'].split('\n') if n['body'] else []
   if kind=='actor':
    cx=x+w/2;svg.extend([f'<circle cx="{cx}" cy="{y+18}" r="15" fill="white" stroke="{GREEN}" stroke-width="2"/>',f'<path d="M {cx} {y+33} V {y+73} M {cx-28} {y+47} H {cx+28} M {cx} {y+73} L {cx-25} {y+103} M {cx} {y+73} L {cx+25} {y+103}" fill="none" stroke="{GREEN}" stroke-width="2"/>']);
    for j,t in enumerate(title.split('\n')):txt(cx,y+130+22*j,t,18,True,'middle')
   elif kind=='ellipse':
    svg.append(f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{PALE}" stroke="{GREEN}" stroke-width="2"/>')
    ts=title.split('\n')
    for j,t in enumerate(ts):txt(x+w/2,y+h/2-(len(ts)-1)*11+6+j*23,t,18,False,'middle')
   elif kind=='boundary':
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{GREEN}" stroke-width="2"/>');txt(x+15,y+26,title,18,True)
   else:
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="white" stroke="{GREEN}" stroke-width="2"/>')
    svg.append(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="45" fill="{PALE}"/>');txt(x+14,y+30,title,20,True)
    for j,t in enumerate(lines):txt(x+14,y+72+j*24,t,17)
   style={'actor':'shape=umlActor;','ellipse':'ellipse;','boundary':'fillColor=none;','box':'rounded=0;'}.get(kind,'rounded=0;')
   c=SubElement(root,'mxCell',id=n['id'],value=title+('\n'+n['body'] if n['body'] else ''),style=style+'whiteSpace=wrap;html=0;fillColor='+('none' if kind=='boundary' else '#E8F1E9')+';strokeColor=#174C3C;fontColor=#20312B;fontSize=18;'+('verticalAlign=top;align=left;spacing=12;' if kind=='box' else ''),vertex='1',parent='1');SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'})
  svg.append(f'<text x="35" y="{self.h-20}" font-family="Arial,sans-serif" font-size="15" fill="{MUTED}">Agenda ao Ar Livre • Fase 1 • Luca Romariz e Miguel Silva • Fonte editável: diagrams.net</text></svg>')
  base.with_suffix('.svg').write_text('\n'.join(svg),encoding='utf-8');base.with_suffix('.drawio').write_bytes(tostring(mx,encoding='utf-8',xml_declaration=True))
 def pdf(self):
  buf=io.BytesIO();pw,ph=landscape(A3);c=canvas.Canvas(buf,pagesize=(pw,ph));c.setTitle(self.title)
  scale=min((pw-60)/self.w,(ph-60)/self.h);ox=(pw-self.w*scale)/2;oy=(ph-self.h*scale)/2
  c.translate(ox,oy);c.scale(scale,scale)
  def col(v):return colors.HexColor(v)
  def text(x,y,t,size=18,bold=False,center=False):
   c.setFillColor(col(INK));c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
   (c.drawCentredString if center else c.drawString)(x,self.h-y,t)
  c.setStrokeColor(col(MUTED));c.setLineWidth(2)
  for e in self.edges:
   c.setDash([8,5] if e['dash'] else [])
   pts=e['points'];p=c.beginPath();p.moveTo(pts[0][0],self.h-pts[0][1])
   for x,y in pts[1:]:p.lineTo(x,self.h-y)
   c.drawPath(p);c.setDash([])
   if e['arrow']:
    x,y=pts[-1];px,py=pts[-2];a=math.atan2(y-py,x-px)
    for d in [-.45,.45]:c.line(x,self.h-y,x-12*math.cos(a+d),self.h-y+12*math.sin(a+d))
   if e['label']:
    a,b=pts[len(pts)//2-1],pts[len(pts)//2];text((a[0]+b[0])/2,(a[1]+b[1])/2+22,e['label'],15,center=True)
   for s,p,q in [(e['start'],pts[0],pts[1]),(e['end'],pts[-1],pts[-2])]:
    if s:
     dx=q[0]-p[0];dy=q[1]-p[1];l=max(1,math.hypot(dx,dy));text(p[0]+40*dx/l,p[1]+40*dy/l-12,s,17,True,True)
  for n in self.nodes:
   x,y,w,h=n['x'],n['y'],n['w'],n['h'];kind=n['kind'];c.setStrokeColor(col(GREEN));c.setFillColor(colors.white)
   if kind=='actor':
    cx=x+w/2;c.circle(cx,self.h-y-18,15,fill=1);c.line(cx,self.h-y-33,cx,self.h-y-73);c.line(cx-28,self.h-y-47,cx+28,self.h-y-47);c.line(cx,self.h-y-73,cx-25,self.h-y-103);c.line(cx,self.h-y-73,cx+25,self.h-y-103)
    for j,t in enumerate(n['title'].split('\n')):text(cx,y+130+j*22,t,18,True,True)
   elif kind=='ellipse':
    c.setFillColor(col(PALE));c.ellipse(x,self.h-y-h,x+w,self.h-y,fill=1)
    ts=n['title'].split('\n')
    for j,t in enumerate(ts):text(x+w/2,y+h/2-(len(ts)-1)*11+6+j*23,t,18,center=True)
   elif kind=='boundary':c.rect(x,self.h-y-h,w,h,fill=0);text(x+15,y+26,n['title'],18,True)
   else:
    c.rect(x,self.h-y-h,w,h,fill=1);c.setFillColor(col(PALE));c.rect(x+1,self.h-y-45,w-2,44,fill=1,stroke=0);text(x+14,y+30,n['title'],20,True)
    for j,t in enumerate(n['body'].split('\n') if n['body'] else []):text(x+14,y+72+j*24,t,17)
  text(35,38,self.title,26,True);text(35,self.h-20,'Agenda ao Ar Livre | Fase 1 | Luca Romariz e Miguel Silva | Prancha de modelagem',15);c.showPage();c.save();return buf.getvalue()

def diagrams():
 out={}
 # UML use cases, grouped for readable actor associations.
 d=Diagram('Diagrama UML de casos de uso',1400,1120)
 d.box('limite',225,70,950,990,'Agenda ao Ar Livre',kind='boundary')
 d.box('vis',30,120,130,150,'Visitante',kind='actor');d.box('part',30,580,150,150,'Participante',kind='actor');d.box('org',1230,600,150,150,'Organizador',kind='actor');d.box('met',1230,165,150,150,'Open-Meteo',kind='actor');d.box('cli',25,890,160,150,'Cliente de API',kind='actor')
 positions={'UC01':(280,125,'Criar conta / entrar'),'UC02':(280,270,'Pesquisar e consultar'),'UC03':(805,170,'Consultar previsão'),'UC04':(805,360,'Manter locais'),'UC05':(805,495,'Manter atividades'),'UC06':(280,460,'Inscrever-se'),'UC07':(280,610,'Minhas inscrições'),'UC08':(280,760,'Cancelar inscrição'),'UC09':(805,690,'Cancelar atividade'),'UC10':(805,865,'Gerar relatório'),'UC11':(280,940,'Consultar API pública')}
 for id,(x,y,t) in positions.items():d.box(id,x,y,315,82,id+'\n'+t,kind='ellipse')
 for uc,ay in [('UC01',165),('UC02',185)]:x,y,_=positions[uc];d.edge('vis',uc,[(160,ay),(200,ay),(200,y+41),(280,y+41)])
 for uc,ay in [('UC06',620),('UC07',640),('UC08',660)]:x,y,_=positions[uc];d.edge('part',uc,[(180,ay),(210,ay),(210,y+41),(280,y+41)])
 for uc,ay in [('UC04',620),('UC05',640),('UC09',660),('UC10',680)]:x,y,_=positions[uc];d.edge('org',uc,[(1230,ay),(1197,ay),(1197,y+41),(1120,y+41)])
 d.edge('cli','UC11',[(185,965),(280,981)]);d.edge('met','UC03',[(1230,210),(1120,211)])
 d.edge('UC02','UC03',[(595,311),(695,311),(695,211),(805,211)],'<<include>>',dash=True,arrow=True)
 out['docs/modelagem/casos-de-uso/casos-de-uso']=d
 d=Diagram('Arquitetura UML de componentes',1400,890)
 for args in [('browser',45,130,310,130,'<<component>> Navegador','HTML / CSS / formulários'),('view',460,130,350,150,'<<component>> Web Django','Views + templates + sessão\nCSRF / forms / autorização'),('api',460,360,350,150,'<<component>> API DRF','GET /api/v1/\nSerializers / filtros / throttle'),('client',45,370,310,120,'<<component>> Cliente API','Terceiros / HTTP JSON'),('domain',940,130,390,160,'<<component>> Domínio','Agenda / inscrições / relatório\nTransações / regras / permissões'),('orm',950,380,370,130,'<<component>> ORM','Models / migrations\nPostgreSQL'),('weather',460,655,350,145,'<<component>> Meteorologia','Validação / timeout / cache\nCliente HTTPS'),('external',950,660,370,120,'<<external>> Open-Meteo','Previsão diária / JSON')]:d.box(*args)
 d.edge('browser','view',[(355,195),(460,195)],'HTTPS',arrow=True);d.edge('client','api',[(355,425),(460,425)],'JSON',arrow=True)
 d.edge('view','domain',[(810,205),(940,205)],arrow=True);d.edge('api','domain',[(810,420),(870,420),(870,260),(940,260)],arrow=True)
 d.edge('domain','orm',[(1135,290),(1135,380)],'ORM',arrow=True)
 d.edge('view','weather',[(460,245),(395,245),(395,710),(460,710)],arrow=True);d.edge('api','weather',[(650,510),(650,655)],arrow=True)
 d.edge('weather','external',[(810,725),(950,725)],'HTTPS',arrow=True)
 d.edge('weather','orm',[(810,775),(880,775),(880,490),(950,490)],'Cache de banco',arrow=True)
 out['docs/arquitetura/componentes']=d
 tables=json.loads((ROOT/'docs/modelagem/banco-de-dados/modelo.json').read_text())
 for name,logical in [('diagrama-er',False),('modelo-logico',True),('diagrama-de-classes',False)]:
  isclass=name=='diagrama-de-classes';d=Diagram(('Diagrama UML de classes' if isclass else 'Modelo lógico - tabelas e chaves' if logical else 'Diagrama entidade-relacionamento'),1500,1250 if logical else 1000)
  positions={'Usuario':(40,90,390,315 if logical else 180),'Local':(1060,90,390,315 if logical else 180),'Categoria':(1060,550 if logical else 405,390,125),'Atividade':(500,490 if logical else 365,440,430 if logical else 200),'Inscricao':(40,830 if logical else 725,390,290 if logical else 180)}
  for t,(x,y,w,h) in positions.items():
   if logical:body='\n'.join(f'{field}: {typ}'+(' [PK]' if 'PK;' in rule else ' [FK]' if 'FK ' in rule else '') for field,typ,rule in tables[t])
   else:
    names={'Usuario':'id [PK]\nnome / email','Local':'id [PK]\nendereço / coordenadas','Categoria':'id [PK]\nnome','Atividade':'id [PK]\ninício / término / capacidade\nsituação','Inscricao':'id [PK]\nsituação / datas'};body=names[t]
   d.box(t,x,y,w,h,t,body)
  ua=405 if logical else 270;la=405 if logical else 270;ay=490 if logical else 365;ah=430 if logical else 200;iy=830 if logical else 725;cy=550 if logical else 405
  d.edge('Usuario','Local',[(430,150),(1060,150)],'possui','1','0..*')
  d.edge('Usuario','Atividade',[(430,ua-40),(470,ua-40),(470,ay+80),(500,ay+80)],'organiza','1','0..*')
  d.edge('Local','Atividade',[(1190,la),(1190,ay-35),(855,ay-35),(855,ay)],'recebe','1','0..*')
  d.edge('Categoria','Atividade',[(1060,cy+65),(940,cy+65)],'classifica','1','0..*')
  d.edge('Usuario','Inscricao',[(140,ua),(140,iy)],'faz','1','0..*')
  d.edge('Atividade','Inscricao',[(700,ay+ah),(700,iy+(170 if logical else 100)),(430,iy+(170 if logical else 100))],'recebe','1','0..*')
  path='docs/modelagem/classes/'+name if isclass else 'docs/modelagem/banco-de-dados/'+name
  out[path]=d
 for p,d in out.items():d.save(p)
 return out

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyAgenda',fontName='Helvetica',fontSize=10,leading=15,spaceAfter=8,textColor=colors.HexColor(INK),splitLongWords=True))
styles.add(ParagraphStyle(name='CellAgenda',fontName='Helvetica',fontSize=8.5,leading=12,spaceAfter=0,textColor=colors.HexColor(INK),splitLongWords=True))
styles.add(ParagraphStyle(name='HAgenda',fontName='Helvetica-Bold',fontSize=16,leading=20,spaceBefore=15,spaceAfter=9,textColor=colors.HexColor(GREEN),keepWithNext=True))
styles.add(ParagraphStyle(name='SubAgenda',fontName='Helvetica-Bold',fontSize=11,leading=15,spaceBefore=10,spaceAfter=7,textColor=colors.HexColor(GREEN),keepWithNext=True))
styles.add(ParagraphStyle(name='TitleAgenda',fontName='Helvetica-Bold',fontSize=27,leading=32,spaceBefore=6,spaceAfter=18,textColor=colors.HexColor(GREEN)))
def inline(t):
 t=escape(t).replace('→',' -&gt; ').replace('≤','&lt;=').replace('≥','&gt;=').replace('—','-').replace('–','-')
 t=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',t);t=re.sub(r'`([^`]+)`',r'<font name="Courier">\1</font>',t)
 t=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m[1]+' ('+m[2]+')',t)
 return t

def make_pdf(md,figures=[]):
 path=ROOT/md;target=path.with_suffix('.pdf');story=[];lines=path.read_text().splitlines();i=0
 while i<len(lines):
  s=lines[i].strip();i+=1
  if not s:continue
  if s.startswith('!['):
   story.append(Paragraph('Diagrama ou prancha visual disponível ao final deste documento; fonte editável e SVG na mesma pasta.',styles['BodyAgenda']));continue
  if s.startswith('```'):
   code=[]
   while i<len(lines) and not lines[i].startswith('```'):code+=textwrap.wrap(lines[i],82,replace_whitespace=False,drop_whitespace=False) or [''];i+=1
   i+=1
   for l in code:story.append(Paragraph(escape(l).replace(' ','&#160;'),ParagraphStyle('code',fontName='Courier',fontSize=7.5,leading=10,spaceAfter=0)))
   story.append(Spacer(1,10));continue
  if s.startswith('|'):
   rows=[s]
   while i<len(lines) and lines[i].strip().startswith('|'):rows.append(lines[i].strip());i+=1
   cells=[]
   for r in rows:
    parts=[p.strip() for p in r.strip('|').split('|')]
    if all(re.fullmatch('[: -]+',p) for p in parts):continue
    cells.append([Paragraph(inline(p),styles['CellAgenda']) for p in parts])
   n=max(map(len,cells));width=(A4[0]-92)/n
   table=Table(cells,colWidths=[width]*n,repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(PALE)),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor(GREEN)),('LINEBELOW',(0,1),(-1,-1),.4,colors.HexColor('#d7dfd8')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story+=[table,Spacer(1,10)];continue
  if s.startswith('# '):style=styles['TitleAgenda'];s=s[2:]
  elif s.startswith('## '):
   if re.match(r'## UC\d+',s):story.append(PageBreak())
   style=styles['HAgenda'];s=s[3:]
  elif s.startswith('### '):style=styles['SubAgenda'];s=s[4:]
  else:style=styles['BodyAgenda'];s=('• '+s[2:] if s.startswith('- ') else s)
  story.append(Paragraph(inline(s),style))
 title=lines[0].lstrip('# ')
 def footer(c,doc):
  c.saveState();c.setStrokeColor(colors.HexColor(GREEN));c.line(46,A4[1]-37,A4[0]-46,A4[1]-37);c.setFont('Helvetica',8);c.setFillColor(colors.HexColor(MUTED));c.drawString(46,A4[1]-29,'AGENDA AO AR LIVRE  /  ENTREGA 1');c.drawString(46,27,'Luca Romariz e Miguel Silva  |  '+title[:58]);c.drawRightString(A4[0]-46,27,str(doc.page));c.restoreState()
 buf=io.BytesIO();doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=46,leftMargin=46,topMargin=57,bottomMargin=49,title=title,author='Luca Romariz e Miguel Silva - elaborado com auxílio de IA');doc.build(story,onFirstPage=footer,onLaterPages=footer)
 writer=PdfWriter();writer.append(PdfReader(io.BytesIO(buf.getvalue())))
 for f in figures:writer.append(PdfReader(io.BytesIO(f.pdf())))
 if md == 'docs/prototipos/identidade-e-prototipos.md':
  images_buf=io.BytesIO()
  c=canvas.Canvas(images_buf,pagesize=landscape(A3))
  pw,ph=landscape(A3)
  titles=['Explorar atividades','Detalhe e previsão','Acesso','Minhas inscrições','Organizar atividades','Nova atividade','Locais','Relatórios']
  screenshots=sorted((ROOT/'docs/prototipos').glob('[0-9][0-9]-*.png'))
  if len(screenshots)!=8:raise ValueError('São necessárias oito capturas das telas.')
  for title,screenshot in zip(titles,screenshots):
   c.setFillColor(colors.HexColor(GREEN));c.setFont('Helvetica-Bold',18)
   c.drawString(35,ph-35,title)
   im=ImageReader(str(screenshot));iw,ih=im.getSize()
   scale=min((pw-70)/iw,(ph-95)/ih)
   c.drawImage(im,(pw-iw*scale)/2,40,width=iw*scale,height=ih*scale)
   c.setFillColor(colors.HexColor(MUTED));c.setFont('Helvetica',9)
   c.drawString(35,20,'Agenda ao Ar Livre | Protótipo da Entrega 1 | Dados fictícios')
   c.showPage()
  c.save();writer.append(PdfReader(io.BytesIO(images_buf.getvalue())))
 writer.write(target);return target

if __name__=='__main__':
 ds=diagrams()
 docs=[('docs/README.md',[]),('docs/visao/visao.md',[]),('docs/modelagem/casos-de-uso/especificacoes-casos-de-uso.md',[ds['docs/modelagem/casos-de-uso/casos-de-uso']]),('docs/arquitetura/arquitetura.md',[ds['docs/arquitetura/componentes']]),('docs/modelagem/classes/diagrama-de-classes.md',[ds['docs/modelagem/classes/diagrama-de-classes']]),('docs/modelagem/banco-de-dados/diagrama-er.md',[ds['docs/modelagem/banco-de-dados/diagrama-er']]),('docs/modelagem/banco-de-dados/modelo-logico.md',[ds['docs/modelagem/banco-de-dados/modelo-logico']]),('docs/api/contrato-api.md',[]),('docs/api/integracao-externa.md',[]),('docs/prototipos/identidade-e-prototipos.md',[]),('docs/planejamento/planejamento.md',[])]
 writer=PdfWriter()
 for md,figs in docs:
  p=make_pdf(md,figs);writer.append(str(p),outline_item=p.stem);print(p.relative_to(ROOT),len(PdfReader(p).pages),'páginas')
 writer.add_metadata({'/Title':'Agenda ao Ar Livre - Entrega 1','/Author':'Luca Romariz e Miguel Silva - assistência de IA declarada'})
 writer.write(ROOT/'docs/entrega-1.pdf')
 print('Consolidado:',len(writer.pages),'páginas')
