from pylode import OntDoc, PylodeError
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import DCTERMS, RDFS
import os

def build(ontology_file, output_dir):
    """Build HTML documentation from TTL ontology file"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Create OntDoc instance
        doc = OntDoc(ontology_file)
        
        # Generate HTML content
        html_content = doc.make_html()
        
        # Write to output file
        output_file = os.path.join(output_dir, 'index.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Documentation generated: {output_file}")
        
    except PylodeError as e:
        if "title property" in str(e):
            print(f"Error: {e}")
            print("Adding a default title to the ontology...")
            
            # Load the ontology and add a title
            g = Graph()
            g.parse(ontology_file, format='turtle')
            
            # Find the ontology URI (usually the first subject that's an ontology)
            ontology_uri = None
            for s, p, o in g:
                if str(p).endswith('#type') and str(o).endswith('Ontology'):
                    ontology_uri = s
                    break
            
            if ontology_uri:
                # Add a title
                g.add((ontology_uri, DCTERMS.title, Literal("Generated Ontology Documentation")))
                
                # Save the modified ontology
                temp_file = ontology_file + '.tmp'
                g.serialize(temp_file, format='turtle')
                
                # Try again with the modified file
                doc = OntDoc(temp_file)
                html_content = doc.make_html()
                
                output_file = os.path.join(output_dir, 'index.html')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"Documentation generated with default title: {output_file}")
                
                # Clean up temp file
                os.remove(temp_file)
            else:
                print("Could not find ontology URI to add title")
        else:
            raise e

if __name__ == "__main__":
    build("generated/ontology.ttl", "generated/docs")
