# This Python file uses the following encoding: utf-8
from aula.utils.tools import classebuida
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.models import Group
from aula.apps.usuaris.models import User2Professor


def calcula_menu( user , path ):
    
    if user is None:
        return
    
    di = Group.objects.get_or_create(name= 'direcció' )[0] in user.groups.all()
    pr = Group.objects.get_or_create(name= 'professors' )[0] in user.groups.all()
    pl = Group.objects.get_or_create(name= 'professional' )[0] in user.groups.all()
    co = Group.objects.get_or_create(name= 'consergeria' )[0] in user.groups.all()
    al = Group.objects.get_or_create(name= 'alumne' )[0] in user.groups.all()
    pg = Group.objects.get_or_create(name= 'psicopedagog' )[0] in user.groups.all()
    tu = pr and ( User2Professor( user).tutor_set.exists() or User2Professor( user).tutorindividualitzat_set.exists() )
    
    tots = di or pr or pl or co or al or pg

    nom_path = resolve( path ).url_name

    menu = { 'items':[], 'subitems':[], 'subsubitems':[], }
    
    try:
        menu_id, submenu_id, subsubmenu_id = nom_path.split( '__' )[:3]
    except:
        return menu
    
    arbre = (
               #--Aula--------------------------------------------------------------------------
               ('aula', 'Aula', 'blanc__blanc__blanc', pr, 
                  (
                      ("Presencia", 'aula__horari__horari', pr, None ),
                      ("Alumnes", 'aula__alumnes__alumnes_i_assignatures', pr, None ),
                      ("Incidències", 'aula__incidencies__blanc', pr,
                          ( 
                            ("Incidències Recollides", 'aula__incidencies__les_meves_incidencies', pr, ),
                            ("Nova Incidència", 'aula__incidencies__posa_incidencia', pr, ),
                            ("Recull Expulsió", 'aula__incidencies__posa_expulsio', pr, ),
                          ),                        
                      ),                                      
                      ("Matèries", 'aula__materies__blanc', pr, 
                          ( 
                            ("Llistat entre dates", 'aula__materies__assistencia_llistat_entre_dates', pr, ),
                            ("Calculadora UF", 'aula__materies__calculadora_uf', pr, )
                          )
                      ),                                      
                   )
               ),

               #--Tutoria--------------------------------------------------------------------------
               ('tutoria', 'Tutoria', 'tutoria__actuacions__list', tu ,
                  (
                      ("Actuacions", 'tutoria__actuacions__list', tu, None ),
                      ("Justificar", 'tutoria__justificar__pre_justificar', tu, None ),                                      
                      ("Cartes", 'tutoria__cartes_assistencia__gestio_cartes', tu, None ),                                      
                      ("Alumnes", 'tutoria__alumnes__list', tu, None ),
                      ("Assistència", 'tutoria__assistencia__list_entre_dates', tu, None ),                                      
                      ("Informe", 'tutoria__alumne__informe_setmanal', tu, None ),                                      
                      ("Portal", 'tutoria__relacio_families__dades_relacio_families', tu, None ),
                      ("Seguiment", 'tutoria__seguiment_tutorial__formulari', tu, None ),                                      
                   )
               ),
             
               #--psicopedagog--------------------------------------------------------------------------
               ('psico', 'Psicopedagog', 'psico__informes_alumne__list', pg or di,
                  (
                      ("Alumne", 'psico__informes_alumne__list', pg or di , None ),
                      ("Actuacions", 'psico__actuacions__list', pg or di , None ),
                   )
               ),
             
               #--Coord.Pedag--------------------------------------------------------------------------
               ('coordinacio_pedagogica', 'Coord.Pedag', 'coordinacio_pedagogica__qualitativa__blanc', di,
                  (
                      ("Qualitativa", 'coordinacio_pedagogica__qualitativa__blanc', di , 
                          (
                              ("Avaluacions", 'coordinacio_pedagogica__qualitativa__avaluacions', di ,  ),
                              ("Items", 'coordinacio_pedagogica__qualitativa__items', di ,  ),
                              ("Resultats", 'coordinacio_pedagogica__qualitativa__resultats_qualitatives', di ,  ),
                          ),
                      ),
                   ),
               ),
  
               #--Coord.Alumnes--------------------------------------------------------------------------
               ('coordinacio_alumnes', 'Coord.Alumnes', 'coordinacio_alumnes__ranking__list', di,
                  (
                      ("Alertes Incidències", 'coordinacio_alumnes__ranking__list', di , None ),
                      ("Alertes Assistència", 'coordinacio_alumnes__assistencia_alertes__llistat', di , None ),
                      ("Cartes", 'coordinacio_alumnes__assistencia__cartes', di , None ),
                      ("Expulsions del Centre", 'coordinacio_alumnes__explusions_centre__expulsions', di , None ),
                      ("Passa llista grup", 'coordinacio_alumnes__presencia__passa_llista_a_un_grup_tria', di , None ),
                      ("Impressió Massiva Faltes i Incidències", 'coordinacio_alumnes__alumne__informe_faltes_incidencies', di , None ),
                   )
               ),

               #--Coord.Profess.--------------------------------------------------------------------------
               ('professorat', 'Coord.Prof', 'professorat__baixes__blanc', di,
                  (
                      ("Feina Absència", 'professorat__baixes__blanc', di ,
                         (
                            ('Posar feina', 'professorat__baixes__complement_formulari_tria', di),
                            ('Imprimir feina', 'professorat__baixes__complement_formulari_impressio_tria' ,di),
                         ), 
                      ),
                      ("Tutors", 'professorat__tutors__blanc', di ,
                         (
                            ('Tutors Grups', 'professorat__tutors__tutors_grups', di),
                            ('Tutors individualitzat', 'professorat__tutors__tutors_individualitzats', di),
                         ), 
                      ),
                   )
               ),

               #--Administració--------------------------------------------------------------------------
               ('administracio', 'Admin', 'administracio__sincronitza__blanc', di,
                  (
                      ("Sincronitza", 'administracio__sincronitza__blanc', di , 
                        (
                          ("Alumnes", 'administracio__sincronitza__saga', di ,  ),
                          ("Horaris", 'administracio__sincronitza__kronowin', di ,  ),
                          ("Reprograma", 'administracio__sincronitza__regenerar_horaris', di ,  ),
                        ),
                      ),
                      ("Reset Passwd", 'administracio__professorat__reset_passwd', di , None ),
                      ("Càrrega Inicial", 'administracio__configuracio__carrega_inicial', di , None ),
                   )
               ),
             
               #--Consergeria--------------------------------------------------------------------------
               ('consergeria', 'Psicopedagog', 'consergeria__missatges__envia_tutors', co,
                  (
                      ("Missatge a tutors", 'consergeria__missatges__envia_tutors', co , None ),
                   )
               ),

               #--Varis--------------------------------------------------------------------------
               ('varis', 'Ajuda', 'varis__elmur__veure', tots,
                  (
                      ("Notificacions", 'varis__elmur__veure', tots , None ),
                      ("Avisos de Seguretat", 'varis__avisos__envia_avis_administradors', tots , None ),
                      ("About", 'varis__about__about', tots , None ),                      
                   )
               ),

             )
    
    for item_id, item_label, item_url, item_condicio, subitems in arbre:

        if not item_condicio:
            continue
        actiu = ( menu_id == item_id )
        item = classebuida()
        item.label = item_label
        item.url = reverse( item_url )
        item.active = 'active' if actiu else ''
        menu['items'].append( item )
        
        if actiu:
            for subitem_label, subitem_url, subitem__condicio, subsubitems in subitems:
                if not subitem__condicio:
                    continue
                actiu = ( submenu_id == subitem_url.split('__')[1] )
                subitem = classebuida()
                subitem.label = subitem_label
                subitem.url = reverse( subitem_url ) 
                subitem.active = 'active' if actiu else ''
                menu['subitems'].append(subitem)
                subitem.subsubitems = []
                if subsubitems:
                    for subitem_label, subitem_url, subitem__condicio in subsubitems:
                        subsubitem = classebuida()
                        subsubitem.label = subitem_label
                        subsubitem.url = reverse( subitem_url ) 
                        subitem.subsubitems.append(subsubitem)
                    if actiu and subsubmenu_id == 'blanc':
                        menu['subsubitems'] = subitem.subsubitems

    return menu


'''

professorat__baixes__complement_formulari_impressio_tria
professorat__baixes__complement_formulari_imprimeix
professorat__baixes__complement_formulari_omple
professorat__baixes__complement_formulari_tria
professorat__professors__list
professorat__tutors__gestio_alumnes_tutor
professorat__tutors__tutors_grups
professorat__tutors__tutors_individualitzats


coordinacio_alumnes__assistencia_alertes__llistat
coordinacio_alumnes__assistencia__cartes
coordinacio_alumnes__explusions_centre__carta
coordinacio_alumnes__explusions_centre__edicio
coordinacio_alumnes__explusions_centre__esborrar
coordinacio_alumnes__explusions_centre__expulsar
coordinacio_alumnes__explusions_centre__expulsio
coordinacio_alumnes__explusions_centre__expulsio
coordinacio_alumnes__explusions_centre__expulsions
coordinacio_alumnes__explusions_centre__expulsions
coordinacio_alumnes__explusions_centre__expulsions_excel
coordinacio_alumnes__presencia__passa_llista_a_un_grup_tria
coordinacio_alumnes__ranking__list
coordinacio_alumnes__seguiment_tutorial__preguntes

administracio__configuracio__assigna_franges_kronowin
administracio__configuracio__assigna_grups
administracio__configuracio__assigna_grups_kronowin
administracio__professorat__reset_passwd
administracio__sincronitza__duplicats
administracio__sincronitza__fusiona
administracio__sincronitza__kronowin
administracio__sincronitza__regenerar_horaris
administracio__sincronitza__saga

coordinacio_pedagogica__qualitativa__avaluacions
coordinacio_pedagogica__qualitativa__items
coordinacio_pedagogica__qualitativa__report

aula__materies__assistencia_llistat_entre_dates
aula__materies__calculadora_uf

aula__horari__afegir_alumnes
aula__horari__afegir_guardia
 aula__horari__alumnes_i_assignatures
aula__horari__elimina_incidencia
aula__horari__esborrar_guardia
aula__horari__feina
aula__horari__horari
aula__horari__horari
aula__horari__hora_sense_alumnes
aula__horari__passa_llista
aula__horari__posa_incidencia
aula__horari__treure_alumnes
aula__incidencies__edita_expulsio
aula__incidencies__elimina_incidencia
aula__incidencies__les_meves_incidencies
 aula__incidencies__posa_expulsio
aula__incidencies__posa_expulsio_per_acumulacio
aula__incidencies__posa_expulsio_w2
 aula__incidencies__posa_incidencia
aula__qualitativa__entra_qualitativa
aula__qualitativa__les_meves_avaulacions_qualitatives
aula__qualitativa__resultats_qualitatives


tutoria__actuacions__alta
tutoria__actuacions__edicio
tutoria__actuacions__esborrat
 tutoria__actuacions__list
tutoria__actuacions__list_entre_dates
tutoria__alumne__detall
tutoria__alumne__informe_faltes_incidencies
tutoria__alumne__informe_setmanal
tutoria__alumne__informe_setmanal_print
tutoria__alumnes__list
tutoria__cartes_assistencia__esborrar_carta
tutoria__cartes_assistencia__gestio_cartes
tutoria__cartes_assistencia__imprimir_carta
tutoria__cartes_assistencia__imprimir_carta_no_flag
tutoria__cartes_assistencia__nova_carta
tutoria__justificar__by_pk_and_date
tutoria__justificar__justificador
tutoria__justificar__next
 tutoria__justificar__pre_justificar
tutoria__obsolet__treure
tutoria__relacio_families__bloqueja_desbloqueja
tutoria__relacio_families___configura_connexio
tutoria__relacio_families__dades_relacio_families
tutoria__relacio_families__envia_benvinguda
 tutoria__seguiment_tutorial__formulari
        


nologin__usuari__login
nologin__usuari__recover_password
nologin__usuari__send_pass_by_email
obsolet__tria_alumne
psico__informes_alumne
relacio_families__configuracio__canvi_parametres
'relacio_families__informe__el_meu_informe'),
relacio_families__informe__el_meu_informe
triaAlumneAlumneAjax
triaAlumneCursAjax
triaAlumneGrupAjax

usuari__dades__canvi
usuari__dades__canvi_passwd
usuari__impersonacio__impersonacio
usuari__impersonacio__reset

varis__todo__del
varis__todo__edit
varis__todo__edit_by_pk
varis__todo__list
'''
        
                