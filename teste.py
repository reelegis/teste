import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
import numpy
import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
from pathlib import Path

# source venv/bin/activate


#st.text('Aqui você escolhe o seu/sua Deputado/a Federal!')

st.text("Versão beta 🐟 v.0.0.2")

st.text('Última atualização em 02/09/2022')

## base de dados do político
#@st.cache(ttl=60*60*24)
@st.cache(ttl=60*60*24)
def load_data():
    data = pd.read_excel('[atualizacao]bd-reelegis-camara-CORRIGIDO.xlsx', index_col=0)
    return data

df = load_data()

#df = df.dropna() #lida com todos os espacos vazios dos dados

st.markdown('No dia 2 de outubro de 2022 teremos novas eleições. É uma oportunidade valiosa para renovar ou premiar a atual composição do Congresso Nacional. Pensando nisso, apresentamos a plataforma reeLegis! Com o uso de aprendizagem computacional, ela permite analisar e comparar a atuação de todos os Deputados e Deputadas Federais que buscam a reeleição. **E aí? Vai reeleger ou renovar?**')

st.markdown('[Aqui, você pode retornar ao site.](https://reelegis.netlify.app)')

#st.markdown(f'Agora em outubro, além de votar para presidente e governador, você também escolherá quem deve ocupar as cadeiras no Legislativo. Pensando nisso, a plataforma **reeLegis** ajuda você a observar quais temas o/a Deputado/a apresentou em proposta legislativa. De modo mais claro, traduzimos as propostas apresentadas pelos/as Parlamentares em **temas** como Saúde, Trabalho e Educação, para que você possa escolher o político ou o partido, para que assim você analise quem mais apresentou as propostas sobre temas que você considera importante. Utilizando técnicas de aprendizado de máquina, após o tratamento e filtragem dos dados, obtivemos {len(df.index)} propostas legislativas apresentadas pelos parlamentares entre 2019 e 2022. Você pode consultar nossa metodologia [retornando ao nosso site principal](https://reelegis.netlify.app).')

#st.markdown('Boa busca e esperamos que ajude na escolha de um voto mais consciente!')
#st.markdown(f'Número de casos {len(df.index)}')
# base de dados do partido

#@st.cache(ttl=60*60*24)
#def load_partido():
#    base_de_dados = pd.read_excel('bd_partido.xlsx', index_col=0)
#    return base

#base = load_partido()

#base = base.dropna()


st.header('Nessas eleições, você prefere votar no Político ou no Partido para o cargo de Deputado/a Federal?')
pol_part = st.radio("Escolha uma opção", ['','Político', 'Partido'], key='1')
df2 = df[df.nomeUrna != 'Não está concorrendo']
df2 = df2.dropna()
if pol_part == 'Político':
    st.header('Onde você vota?')
    uf = df2['estado_extenso_eleicao'].unique()
    uf = np.append(uf, '')
    uf.sort()
    uf_escolha = st.selectbox("Selecione o Estado", uf)
    if uf_escolha != '':
        f_par2 = df2.loc[df2.estado_extenso_eleicao == uf_escolha, :]
        f = pd.DataFrame(f_par2)
        perc = f.nomeUrna.value_counts() #/ len(f) * 100
        parlamentar_do_estado = f_par2['nomeUrna'].unique()
        parlamentar_do_estado = np.append(parlamentar_do_estado, '')
        parlamentar_do_estado.sort()
        st.subheader('Qual Parlamentar você gostaria de visualizar?')
        escolha_parlamentar_do_estado = st.selectbox("Selecione o Parlamentar", parlamentar_do_estado)
        #st.error(f'Caso você não encontre o/a Deputado/a do seu estado, isso é devido ao fato dele/a não estar concorrendo à reeleição, ou não apresentou propostas até o período de nossa coleta (18/07/2022).')
        if escolha_parlamentar_do_estado != '':
            f_par23 = f_par2.loc[f_par2.nomeUrna == escolha_parlamentar_do_estado, :]
            f23 = pd.DataFrame(f_par23)
                    #f.nomeUrna = f.nomeUrna.astype('string')
            perc23 = f23.Tema.value_counts() / len(f23) * 100
                    #contar = f['nomeUrna'].value_counts()
                    #c = sum(contar)
                    #contar = contar/sum()
                    # filter_partido_proposi2 = f_par2.loc[f_par.autor_partido == choice_dep]
            gen_uf = pd.DataFrame(data=f_par23['genero'].value_counts())
            genero = gen_uf['genero']

            if genero.index[0] == 'o Deputado':
                elu_delu = 'Ele'
            else:
                elu_delu = 'Ela'

           

            path = Path(str_path)
            numero = f_par23['numero']
            n = numero.iloc[0]
            n0 = int(n)
            cor_raca = f_par23['cor_raca']
            cor = cor_raca.iloc[0]
            profissao = f_par23['Profissao']
            trabalho = profissao.iloc[0]
            party = f_par23['partido_ext_sigla'].iloc[0]
            bens_depois = f_par23['patrimonio_depois'].iloc[0]
            bens_posteriores = str(bens_depois.replace('.',','))


            def split1000(s, sep='.'):
                return s if len(s) <= 3 else split1000(s[:-3], sep) + sep + s[-3:]
            x=split1000(bens_posteriores)



            y = x[:-4] + x[-3:]
            if y == '0,00':
                y='Ainda não declarado'
                real = ''
            else:
                real = 'R$'

            sex = pd.DataFrame(data=f_par23['sexo'].value_counts())
            sexo = sex['sexo']


           

            #st.subheader(f'Em comparação com os outros parlamentares de {uf_escolha}, {escolha_parlamentar_do_estado}')
            ## grafico destacado aqui!
            st.title('*Ranking* da quantidade de propostas apresentadas pelos/as candidatos/as à reeleição')
            st.info(f'No gráfico a seguir, a barra em azul indica a posição de **{escolha_parlamentar_do_estado}** em comparação com os demais deputados federais em cinza da Unidade Federativa **{uf_escolha}** no que se refere à média de propostas apresentadas por dias de mandato.')


            #perc['posicao'] =
            position = pd.DataFrame(perc)
            #st.write(position.index[0])
            amplitude = len(position)
            #st.write(amplitude)
            position.insert(1,"posicao", range(0,amplitude))
            lugar = position[['nomeUrna', 'posicao']] +1
            l = lugar[(lugar.index == escolha_parlamentar_do_estado)]
            #st.write(l)
            #l = position.loc[position.nomeUrna == escolha_parlamentar_do_estado]
            #l = position.loc[position.nomeUrna == escolha_parlamentar_do_estado, :]
            #st.table(lugar)
            #st.write(lugar.index)

            #posit = l['posicao'].iloc[0]
            #st.info(f'**{escolha_parlamentar_do_estado}** está na {posit}ᵃ posição no *ranking*.')
            #st.table(position)

            #st.subheader(f'{escolha_parlamentar_do_estado}')
            contagem_parlamentares = f.groupby(f.nomeUrna.tolist(),as_index=False).size()

            #st.table(contagem_parlamentares)
            f2 = pd.DataFrame(f_par2[['nomeUrna', 'dias_total']])
            urna_names = f2.groupby(['nomeUrna']).size()
            #dias_contados = f2.groupby(['nomeUrna', 'dias_total']).size()

            dias_nome = pd.DataFrame(f_par2, columns = ['nomeUrna', 'dias_total'])
            #g=dias_nome.groupby('nomeUrna').agg(set)

            g = dias_nome.groupby('nomeUrna')['dias_total'].apply(lambda x: float(np.unique(x)))
            #g = dias_nome.groupby('nomeUrna')['dias_total'].nunique()
            d = pd.concat([g, urna_names], axis=1)
            dias = pd.DataFrame(d)
            #percapita = dias['dias_total']/2
            #dias['dias_total'].astype(int)

            #percapita = dias['dias_total']/dias[0]

            #percapita_dias = dias['dias_total']

            #dias['dias_total'] = dias['dias_total'].astype(float)
            result = dias[0]/dias['dias_total']
            #pts = pd.concat([dias[0], result], axis=1)
            r = pd.DataFrame(result)
            #st.table(result)
            r[0] = r[0].rank(ascending=False)
            #re = r[0]

            posit = r.loc[r.index == escolha_parlamentar_do_estado, :]
            p = round(posit.iloc[0], 1)

            d = p//1

            d0 = int(d)
            #st.table(p)
            st.info(f'**{escolha_parlamentar_do_estado}** está na **{d0}ᵃ** posição no *ranking*.')
            #st.text(type(result))
            #st.text(percapita)


            #dias_contados = f2.groupby('nomeUrna')['dias_total'].nunique()

            #urna = pd.DataFrame(dias_contados, columns = ['nomeUrna'])
            #urna.columns=['n_materias']
            #g_sum2 = new2.groupby(['dias_total'])
            #st.table(result)

            #st.table(perc)
            condicao_split_parlamentar = len(contagem_parlamentares.index)
            f2 = pd.DataFrame(f_par2[['nomeUrna', 'dias_total']])
            urna_names = f2.groupby(['nomeUrna']).size()
            #dias_contados = f2.groupby(['nomeUrna', 'dias_total']).size()

            dias_nome = pd.DataFrame(f_par2, columns = ['nomeUrna', 'dias_total'])
            #g=dias_nome.groupby('nomeUrna').agg(set)

            g = dias_nome.groupby('nomeUrna')['dias_total'].apply(lambda x: float(np.unique(x)))
            #g = dias_nome.groupby('nomeUrna')['dias_total'].nunique()
            d = pd.concat([g, urna_names], axis=1)
            dias = pd.DataFrame(d)
            #percapita = dias['dias_total']/2
            #dias['dias_total'].astype(int)

            #percapita = dias['dias_total']/dias[0]

            #percapita_dias = dias['dias_total']

            #dias['dias_total'] = dias['dias_total'].astype(float)
            result2 = dias[0]/dias['dias_total']
            if condicao_split_parlamentar > 29:
                #parl_dep = px.bar(perc, x='nomeUrna', height=1500, width=900,
                #labels=dict(index="Parlamentar", nomeUrna="% Propostas apresentadas"),
                #orientation='h')
                fig1=px.bar(result2, height=1500, labels=dict(index="", value='Quantidade de propostas apresentadas'), orientation='h')
                fig1["data"][0]["marker"]["color"] = ["blue" if c == escolha_parlamentar_do_estado else "#C0C0C0" for c in fig1["data"][0]["y"]]
                fig1.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig1, use_container_width=True)

                first = perc.iloc[:1].round()
                #st.info(f'Na Unidade Federativa {uf_escolha}, {perc.index[0]} foi quem mais apresentou propostas legislativas entre 2019 e 2022, com {first.to_string(index=False)} apresentadas até o dia 18 de julho de 2022.')
                #st.info('Caso queira visualizar a tabela descritiva do gráfico, clique abaixo.')



                    #st.success(sorteio.query("Tema == @random_tema")[["ementa", "keywords"]].sample(n=1).iat[0, 0])

                #grafico_parlamentar_maior = px.bar(perc, x='nomeUrna', height=1500, width=900, #color='nomeUrna',
                #    labels=dict(index="Parlamentar", nomeUrna="% Propostas apresentadas"),
                #    orientation='h')
                #grafico_parlamentar_maior.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})

                #st.plotly_chart(grafico_parlamentar_maior)
                #first = perc.iloc[:1].round()
                #last = perc.iloc[:-1].round()
                #st.write(perc.index[0], "foi quem mais apresentou propostas no Estado selecionado, contando com aproximadamente",
                #first.to_string(index=False) + '% em relação a todos os parlamentares na Unidade Federativa', uf_escolha +
                #'.') # Em contrapartida,', perc.index[-1])
                #st.info('Caso queira visualizar a tabela descritiva do gráfico, clique abaixo.')
            else:
                #parl_dep = px.bar(perc, x='nomeUrna', height=600, width=700,
                #labels=dict(index="Parlamentar", nomeUrna="% Propostas apresentadas"),
                #orientation='h')
                fig1=px.bar(result2, height=600, labels=dict(nomeUrna="", value='Propostas por Dia'), orientation='h')
                fig1["data"][0]["marker"]["color"] = ["blue" if c == escolha_parlamentar_do_estado else "#C0C0C0" for c in fig1["data"][0]["y"]]
                fig1.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig1, use_container_width=True)

                first = perc.iloc[:1].round()
                #st.info(f'Na Unidade Federativa {uf_escolha}, {perc.index[0]} foi quem mais apresentou propostas legislativas entre 2019 e 2022, com {first.to_string(index=False)} apresentadas até o dia 18 de julho de 2022.')
                #st.info('Caso queira visualizar a tabela descritiva do gráfico, clique abaixo.')
            re2 = pd.DataFrame(result2)
            #dias_mandato
            posit2 = re2.loc[re2.index == escolha_parlamentar_do_estado, :]
            #dias_mandato = dias.loc[dias.index==escolha_parlamentar_do_estado, :]
            #di[0]=dias_mandato['dias_total']
            dias_mandado = f_par23['dias_total'].unique()
            days = f_par23['dias_total'].iloc[0]
            ndays = float(days)
            dm=int(ndays)
            #ndias = dias_mandado.iloc[0]
            #ndays = int(ndias)
            #out_arr = np.array_str(dias_mandado)
            p2 = round(posit2.iloc[0], 3)
            n_proposta_uf = f_par23.index
            n_proposta_uf = len(n_proposta_uf)
            df_uf = pd.DataFrame(data=f_par23['Tema'].value_counts())
            df_uf['Tema'] = pd.to_numeric(df_uf['Tema'])
            saliente_uf = df_uf['Tema']
            first = int(perc23.iloc[:1])
            last = perc23.iloc[:-1].round()

            st.info(f'**{escolha_parlamentar_do_estado}** apresentou, *em média*, **{p2.to_string(index=False)}** propostas por dia. Um total de **{str(n_proposta_uf)}** propostas legislativas em **{dm}** dias de mandato parlamentar.')

            st.title(f'Ênfase temática apresentada por {escolha_parlamentar_do_estado}')
            estado_parla = px.bar(perc23, x='Tema', height=500,color='Tema',color_continuous_scale='Sunsetdark',
            # site com as cores: https://plotly.com/python/builtin-colorscales/
            labels=dict(index="Tema", Tema="Ênfase Temática %"), orientation='h')
            estado_parla.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(estado_parla)



            st.info(f'**{escolha_parlamentar_do_estado}** apresentou **{str(n_proposta_uf)} propostas legislativas** ao total. A maior ênfase temática d{genero.index[0]} foi **{saliente_uf.index[0]}**, com aproximadamente **{first}% do total.**')

                ## conhecer as Propostas
            st.title(f'Conheça as propostas apresentadas por {escolha_parlamentar_do_estado}')
                #st.checkbox('Consultar propostas apresentadas deste Parlamentar por tema', False):
            tema = f_par23['Tema'].unique()
            tema = np.append(tema, '')
            tema.sort()
            random_tema = st.radio("Escolha o Tema", tema)
            if random_tema != '':
                random_val = f_par23.loc[f_par23.Tema == random_tema, :]
                sorteio = random_val.loc[random_val.Tema == random_tema]
                maior = pd.DataFrame(sorteio[['ementa', 'maior_prob']]).max()
                ementa_maior=maior.iloc[0]
                probabilidade_maior=int((maior.iloc[1] * 100))
                    #st.write(probabilidade_maior)

                    #max_percent = max(sorteio['maior_prob'].items(), key=lambda i: i[1])
                    #st.write(max_percent)
                ementa = pd.DataFrame(data=random_val['explicacao_tema'].value_counts())
                st.write(ementa.index[0])
                st.write(f'*Esta é uma proposta apresentada por* **{escolha_parlamentar_do_estado}** que trata **{random_tema}**.')
                # A probabilidade de pertencer ao tópico é de {probabilidade_maior}%.
                st.success(ementa_maior)

            #st.title(f"Declaração de bens de {escolha_parlamentar_do_estado}")
            #ano_anterior = 2018
            #ano_eleitoral = 2022
            #bens_antes = f_par23['patrimonio_antes'].iloc[0]
            #bens_anteriores = float(bens_antes)
            #bens_depois = f_par23['patrimonio_depois'].iloc[0]
            #bens_posteriores = float(bens_depois)

            #patrimonio = pd.DataFrame(dict(
            #ano = [ano_anterior, ano_eleitoral],
            #declarado = [bens_anteriores, bens_posteriores]
            #))
            #patri_bens = px.line(patrimonio, x="ano", y="declarado", text="declarado", labels=dict(declarado="R$", ano='Ano'))
            #patri_bens.update_traces(textposition='top center')
            #patri_bens.update_traces(mode='lines')
            #patri_bens.data[0].line.color = "#0000ff"
            #st.plotly_chart(patri_bens)



                    #st.success(sorteio.query("Tema == @random_tema")[["ementa", "keywords"]].sample(n=1).iat[0, 0])
            st.header('📢  Conta pra gente!')
            st.warning('Fique à vontade para nos informar sobre algo que queria ter visto nesta aba ou sobre a plataforma, para melhorarmos no futuro!')
            contact_form = """
            <form action="https://formsubmit.co/reelegis@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Nome" required>
            <input type="email" name="email" placeholder="E-mail" required>
            <textarea name="message" placeholder="Sua mensagem"></textarea>
            <button type="submit">Enviar</button>
            </form>
            """
            st.markdown(contact_form, unsafe_allow_html=True)

            def local_css(file_name):
                with open(file_name) as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            local_css("style.css")

if pol_part == 'Partido':
    st.header('Onde você vota?')
    df = df.dropna()
    uf = df['estado_partido_exercicio'].unique()
    uf = np.append(uf, '')
    uf.sort()
    uf_escolha = st.selectbox("Selecione o Estado", uf)
    if uf_escolha != '':
        f_par2 = df.loc[df.estado_partido_exercicio == uf_escolha, :]
        f = pd.DataFrame(f_par2)
        perc = f.nomeUrna.value_counts() #/ len(f) * 100
        partido_do_estado = f_par2['partido_ext_sigla'].unique()
        partido_do_estado = np.append(partido_do_estado, '')
        partido_do_estado.sort()
        st.subheader('Qual partido você gostaria de visualizar?')
        escolha_partido_do_estado = st.selectbox("Selecione o partido", partido_do_estado)
        #f233 = pd.DataFrame(f_par2)
                #f.nomeUrna = f.nomeUrna.astype('string')
        #perc233 = f233.Tema.value_counts() / len(f233) * 100
        #estado_partido = px.bar(perc233, x='Tema', height=500,color='Tema',color_continuous_scale='Sunsetdark',
        # site com as cores: https://plotly.com/python/builtin-colorscales/
        #labels=dict(index="Tema", Tema="Ênfase Temática %"), orientation='h')
        #estado_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
        #st.plotly_chart(estado_partido, use_container_width=True)
        #st.error(f'Alguns partidos podem não ter sido eleitos na Unidade Federativa {uf_escolha}.')
        if escolha_partido_do_estado != '':
            f_par23 = f_par2.loc[f_par2.partido_ext_sigla == escolha_partido_do_estado, :]
            f23 = pd.DataFrame(f_par23)
                    #f.nomeUrna = f.nomeUrna.astype('string')
            perc23 = f23.Tema.value_counts() / len(f23) * 100
                    #contar = f['nomeUrna'].value_counts()
                    #c = sum(contar)
                    #contar = contar/sum()
                    # filter_partido_proposi2 = f_par2.loc[f_par.autor_partido == choice_dep]

            f = pd.DataFrame(f_par2[['nomeUrna', 'partido_ext_sigla']])
            new = f.groupby(['partido_ext_sigla', 'nomeUrna']).size()#.groupby(['partido_ext_sigla']).size()
            g_sum = new.groupby(['partido_ext_sigla']).sum()
            n = new.groupby(['partido_ext_sigla']).size()
            per = pd.concat([g_sum, n], axis=1)
            percapita = per[0]/per[1]
            per_capita = pd.DataFrame(percapita)
            per_capita.columns=['Taxa per capita']



            #f_par23 = f_par2.loc[f_par2.partido_ext_sigla == escolha_partido_do_estado, :]
            #st.write(partido_selecionado)
            #st.table(per_capita)
            #estado_parla = px.bar(per_capita, x='Taxa per capita', height=500, labels=dict(partido_ext_sigla="Partido"),
            #orientation='h')
            partidos_per = pd.DataFrame(per_capita)
            partidos_per.columns=['Taxa per capita']
            reorder = partidos_per.sort_values(by = 'Taxa per capita', ascending = False)
            partidos_per.Taxa = pd.to_numeric(partidos_per['Taxa per capita'], errors='coerce')
            ppc = partidos_per.sort_values(by='Taxa per capita', ascending=False)
            #st.table(partidos_per)
            first= ppc.iloc[0]
            last = ppc.iloc[-1]
            st.title('*Ranking* da quantidade de propostas apresentadas pelos Partidos')
            #st.title('*Ranking* da quantidade de propostas apresentadas pelos/as candidatos/as à reeleição')
            st.info(f'A barra em azul indica a posição do **{escolha_partido_do_estado}** em comparação com os demais partidos que possuem parlamentares na Câmara Federal da Unidade Federativa **{uf_escolha}** no que se refere à quantidade de propostas apresentadas.')
            partido_selecionado = int(per_capita.loc[escolha_partido_do_estado])
            #st.write(partido_selecionado.index[0])
            #st.write(f'{partido_selecionado.to_string(index=False)}')

            position = pd.DataFrame(ppc)
            amplitude = len(position)
            position.insert(1,"posicao", range(0,amplitude))
            lugar = position[['Taxa per capita', 'posicao']] +1
            l = lugar[(lugar.index == escolha_partido_do_estado)]
            posit = l['posicao'].iloc[0]

            st.info(f'O **{escolha_partido_do_estado}** apresentou, **em média, {partido_selecionado}** propostas por Parlamentar na Unidade Federativa **{uf_escolha}**. No *ranking*, **{escolha_partido_do_estado}** está na **{posit}ᵃ** posição.')



            #st.header(f'Taxa _per capita_ de propostas apresentadas pelo {escolha_partido_do_estado} na Unidade Federativa {uf_escolha}')
            fig_partido=px.bar(per_capita, height=600, labels=dict(partido_ext_sigla="", value='Taxa por parlamentar'), orientation='h')
            fig_partido["data"][0]["marker"]["color"] = ["blue" if c == escolha_partido_do_estado else "#C0C0C0" for c in fig_partido["data"][0]["y"]]
            fig_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_partido,use_container_width=True)


            #estado_parla.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})

            #st.plotly_chart(estado_parla)
            st.success('A _taxa de propostas apresentadas por parlamentar_ leva em consideração o total de projetos apresentados do partido nesta Unidade Federativa dividido pela quantidade de seus parlamentares.')# A opção por esta métrica permite tornar os partidos comparáveis com base na quantidade de seus membros, não indicando necessariamente o valor total de projetos que foram apresentados pelo partido. ')


            #st.info(f'Na Unidade Federativa, **{uf_escolha}** o **{escolha_partido_do_estado}** ap')

            #é o {ppc.index[0]}, com {first.to_string(index=False)}. Isso indica que, em média, 1 parlamentar deste partido apresentou {first.to_string(index=False)} propostas. Em contrapartida, o {ppc.index[-1]} é o partido que menos apresentou propostas, com {last.to_string(index=False)} de taxa _per capita_ no Estado selecionado.')

            st.title(f'Ênfase temática apresentada por {escolha_partido_do_estado}')
            estado_partido = px.bar(perc23, x='Tema', height=500,color='Tema',color_continuous_scale='Sunsetdark',
            # site com as cores: https://plotly.com/python/builtin-colorscales/
            labels=dict(index="Tema", Tema="Ênfase Temática %"), orientation='h')
            estado_partido.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(estado_partido, use_container_width=True)

            n_proposta_uf = f_par23.index
            n_proposta_uf = len(n_proposta_uf)
            df_uf = pd.DataFrame(data=f_par23['Tema'].value_counts())
            saliente_uf = df_uf['Tema']
            first = int(perc23.iloc[:1])
            last = perc23.iloc[:-1].round()


            st.info(f'O **{escolha_partido_do_estado}** apresentou **um total de {str(n_proposta_uf)}** propostas legislativas pela Unidade Federativa **{uf_escolha}**. A maior ênfase temática foi **{saliente_uf.index[0]}**, com aproximadamente **{first}% do total**.')


            ## conhecer as Propostas
            st.header(f'Conheça as propostas apresentadas pelo {escolha_partido_do_estado}')
            #st.checkbox('Consultar propostas apresentadas deste Parlamentar por tema', False):
            tema = f_par23['Tema'].unique()
            tema = np.append(tema, '')
            tema.sort()
            random_tema = st.radio("Escolha o Tema", tema)
            if random_tema != '':
                random_val = f_par23.loc[f_par23.Tema == random_tema, :]
                sorteio = random_val.loc[random_val.Tema == random_tema]
                maior = pd.DataFrame(sorteio[['ementa', 'maior_prob']]).max()
                ementa_maior=maior.iloc[0]
                probabilidade_maior=int((maior.iloc[1] * 100))
                #st.write(probabilidade_maior)

                #max_percent = max(sorteio['maior_prob'].items(), key=lambda i: i[1])
                #st.write(max_percent)
                ementa = pd.DataFrame(data=random_val['explicacao_tema'].value_counts())
                st.write(ementa.index[0])
                st.write(f'*Este é um exemplo de proposta apresentada pelo* **{escolha_partido_do_estado}** *sobre* **{random_tema}**')
                #. A probabilidade de pertencer ao tópico é de {probabilidade_maior}%.')
                st.success(ementa_maior)
                #st.success(sorteio.query("Tema == @random_tema")[["ementa", "keywords"]].sample(n=1).iat[0, 0])
